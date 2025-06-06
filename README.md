# 💸 Simulador de Custos - Databricks na AWS

Bem-vindo ao **Simulador de Custos** para calcular os gastos com Databricks na AWS! Este projeto foi desenvolvido usando **Streamlit** e tem como objetivo estimar os custos de clusters do Databricks na AWS com base em parâmetros como tipo de instância EC2, região, número de workers, horas de uso e volume de armazenamento.

## 🎯 Funcionalidades

- **💻 Estima o custo de instâncias EC2**: Calcula o custo baseado no tipo de instância e região.
- **🔲 Calcula o custo de DBU (Databricks Unit)**: Estima o custo do cluster com base no tipo de plano.
- **🛠 Personalização**: Escolha o número de workers, tempo de uso e volume de armazenamento.
- **📊 Visualização dos custos**: Exibe a estimativa detalhada dos custos por tipo de serviço.
- **📥 Download**: Baixe a estimativa de custo como um arquivo CSV.

## 🧑‍💻 Tecnologias Utilizadas

- **Streamlit**: Framework para criar a interface de usuário interativa.
- **Boto3**: Biblioteca da AWS para interagir com serviços como EC2 e Pricing.
- **Pandas**: Para manipulação e visualização dos dados.
- **AWS Pricing API**: Para consultar os preços das instâncias EC2 na AWS.

## 🔧 Pré-requisitos

Antes de rodar o projeto, certifique-se de ter o seguinte:

- **Python 3.x**: Você pode baixar [aqui](https://www.python.org/downloads/).
- **Conta AWS** com acesso às credenciais (Access Key ID e Secret Access Key).

## 🛠 Instalação

1. **Clone o repositório**:

    ```bash
    git clone https://github.com/seu_usuario/seu_repositorio.git
    cd seu_repositorio
    ```

2. **Crie um ambiente virtual** (recomendado):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Windows use: venv\Scripts\activate
    ```

3. **Instale as dependências**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure suas credenciais AWS** no arquivo `secrets.toml`:

    Crie ou edite o arquivo `secrets.toml` com suas credenciais AWS:

    ```toml
    [aws]
    aws_secret_access_key = "your_aws_secret_access_key"
    aws_access_key_id = "your_aws_access_key_id"
    ```

## 🚀 Como Usar

1. **Execute o aplicativo**:

    Após a instalação, execute o aplicativo com o comando:

    ```bash
    streamlit run app.py
    ```

2. **Interaja com a interface**:

    A interface será aberta no seu navegador, permitindo que você:

    - Escolha o **tipo de cluster** (DBU) e o **tipo de instância EC2**.
    - Selecione a **região AWS** onde a instância será criada.
    - Defina o **número de workers**, **horas de uso** e **volume de armazenamento**.

3. **Obtenha a estimativa de custos**:

    A estimativa de custo será calculada automaticamente. Abaixo você verá o detalhamento de:

    - **Custo DBU**
    - **Custo EC2**
    - **Custo de Armazenamento**

4. **Baixe o CSV**:

    Após visualizar os custos, você pode **baixar a estimativa como um arquivo CSV** clicando no botão de download!

    ![Exemplo de Interface Streamlit](https://your-image-link.com)  <!-- Se tiver imagem da interface, adicione o link aqui -->

## 🗂 Estrutura do Projeto

```plaintext
.
├── app.py               # Arquivo principal com a lógica do Streamlit
├── requirements.txt     # Arquivo com as dependências do projeto
├── secrets.toml         # Arquivo de configurações de credenciais AWS
└── README.md            # Este arquivo
````

## 🤝 Como Contribuir

Contribuições são sempre bem-vindas! Para ajudar a melhorar este projeto, siga os passos abaixo:

1. **Faça um fork** do repositório.
2. **Crie uma nova branch** (`git checkout -b feature-nome-da-feature`).
3. **Implemente a sua feature** ou correção.
4. **Faça um commit** com as mudanças (`git commit -am 'feat: nova funcionalidade'`).
5. **Envie o pull request** explicando suas modificações.

## 📝 Licença

Este projeto é licenciado sob a **MIT License**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📦 Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`:

```txt
streamlit==1.17.0
boto3==1.24.18
pandas==1.4.3
```

---

Obrigado por usar o **Simulador de Custos - Databricks na AWS**! 💸✨
