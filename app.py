import streamlit as st
import boto3
import json
import pandas as pd

st.set_page_config(page_title="Simulador de Custos - Databricks na AWS", page_icon="💸")

AWS_SECRET_ACCESS_KEY = st.secrets.get("aws_secret_access_key")
AWS_ACCESS_KEY_ID = st.secrets.get("aws_access_key_id")

if not AWS_SECRET_ACCESS_KEY or not AWS_ACCESS_KEY_ID:
    st.error("⚠️ Configurações AWS não encontradas. Verifique suas credenciais no arquivo secrets.toml.")
    st.stop()

@st.cache_data(show_spinner=False)
def get_ec2_price(instance_type, region='US East (Ohio)', os='Linux'):
    """
    Obtém o preço de uma instância EC2 com base no tipo de instância, região e sistema operacional especificados.

    Parameters
    ----------
    instance_type : str
        O tipo de instância EC2 (ex. 'm5.large').
    region : str, opcional
        A região AWS onde a instância está localizada, por padrão 'US East (Ohio)'.
    os : str, opcional
        O sistema operacional da instância, por padrão 'Linux'.

    Returns
    -------
    float
        O preço por hora da instância EC2 especificada em USD, ou None se o preço não for encontrado.
    
    Exceptions
    ----------
    Exception
        Caso ocorra qualquer erro durante a obtenção do preço da AWS, retorna None.
    """
    try:
        pricing = boto3.client(
            'pricing',
            region_name='us-east-1',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        response = pricing.get_products(
            ServiceCode='AmazonEC2',
            Filters=[
                {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
                {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': os},
                {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'},
                {'Type': 'TERM_MATCH', 'Field': 'preInstalledSw', 'Value': 'NA'},
                {'Type': 'TERM_MATCH', 'Field': 'capacitystatus', 'Value': 'Used'}
            ],
            MaxResults=1
        )
        price_list = response['PriceList']
        if not price_list:
            return None
        price_item = json.loads(price_list[0])
        terms = price_item['terms']['OnDemand']
        price_dimensions = list(list(terms.values())[0]['priceDimensions'].values())[0]
        return float(price_dimensions['pricePerUnit']['USD'])
    except Exception:
        return None

FALLBACK_PRICES_SAOPAULO = {
    "m5.large": 0.126,
    "m5.xlarge": 0.252,
    "m5.2xlarge": 0.504,
    "c5.xlarge": 0.21,
    "c5.2xlarge": 0.42,
    "r5.xlarge": 0.252,
    "r5.2xlarge": 0.504,
    "i3.xlarge": 0.344,
    "i3.2xlarge": 0.688,
    "m5d.large": 0.144
}

REGIONS = {
    "US East (N. Virginia)": ("us-east-1", "US East (N. Virginia)"),
    "US East (Ohio)": ("us-east-2", "US East (Ohio)"),
    "South America (São Paulo)": ("sa-east-1", "South America (São Paulo)")
}

DBU_PRICES = {
    "Jobs Light": 0.07,
    "Standard": 0.15,
    "Premium": 0.20,
    "Enterprise": 0.25
}

INSTANCE_OPTIONS = [
    "m5.large", "m5.xlarge", "m5.2xlarge",
    "r5.xlarge", "r5.2xlarge",
    "i3.xlarge", "i3.2xlarge",
    "c5.xlarge", "c5.2xlarge",
    "m5d.large"
]

st.title("💸 Simulador de Custos - Databricks na AWS")

cluster_type = st.selectbox("Plano do Cluster (DBU)", list(DBU_PRICES.keys()))
instance_type = st.selectbox("Instância EC2", INSTANCE_OPTIONS)
region_label = st.selectbox("Região AWS", list(REGIONS.keys()))
region_code, region_name = REGIONS[region_label]

num_workers = st.slider("Nº de Workers", 1, 50, 4)
driver_included = st.checkbox("Incluir nó driver?", value=True)
usage_hours = st.slider("Horas de uso", 1, 720, 40)
storage_gb = st.slider("Volume de Armazenamento (GB)", 10, 5000, 100)

if region_code == "sa-east-1":
    st.info("ℹ️ Preço em tempo real não disponível para São Paulo. Usando valores estimados.")
    instance_price = FALLBACK_PRICES_SAOPAULO.get(instance_type, 0.1)
else:
    instance_price = get_ec2_price(instance_type, region=region_name)
    if instance_price is None:
        st.warning(f"⚠️ Preço não encontrado para '{instance_type}' em '{region_label}'. Usando valor estimado.")
        instance_price = FALLBACK_PRICES_SAOPAULO.get(instance_type, 0.1)

total_nodes = num_workers + (1 if driver_included else 0)
dbu_price = DBU_PRICES[cluster_type]

dbu_cost = dbu_price * total_nodes * usage_hours
infra_cost = instance_price * total_nodes * usage_hours
storage_cost = 0.023 * (storage_gb / 720) * usage_hours
total_cost = dbu_cost + infra_cost + storage_cost

st.subheader("📊 Estimativa de Custos")
st.write(f"🔹 DBU: ${dbu_cost:.2f}")
st.text(f"🔹 EC2 ({instance_type}): ${infra_cost:.2f} - {total_nodes} nos x ${instance_price:.3f}/h")
st.write(f"🔹 Armazenamento: ${storage_cost:.2f}")
st.markdown("---")
st.success(f"💰 Total Estimado: ${total_cost:.2f}")

df = pd.DataFrame([{
    "Cluster": cluster_type,
    "Instância": instance_type,
    "Região": region_label,
    "Workers": num_workers,
    "Driver incluso": driver_included,
    "Horas de uso": usage_hours,
    "Storage GB": storage_gb,
    "Custo DBU": round(dbu_cost, 2),
    "Custo EC2": round(infra_cost, 2),
    "Custo Armazenamento": round(storage_cost, 2),
    "Total": round(total_cost, 2)
}])

csv_data = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Baixar estimativa como CSV",
    data=csv_data,
    file_name="estimativa_databricks.csv",
    mime="text/csv"
)
