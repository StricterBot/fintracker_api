# 🏦 FinTrackerAPI

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Uma API RESTful para rastreamento financeiro pessoal, construída com FastAPI e PostgreSQL.

## 📝 Sumário

-   [Sobre o Projeto](#-sobre-o-projeto)
-   [Funcionalidades](#-funcionalidades)
-   [Tecnologias Utilizadas](#-tecnologias-utilizadas)
-   [ Começando](#-começando)
    -   [Pré-requisitos](#pré-requisitos)
    -   [Instalação](#instalação)
-   [ Documentação da API](#-documentação-da-api)
-   [ Migrações de Banco de Dados](#-migrações-de-banco-de-dados)
-   [ Licença](#-licença)
-   [ Contato](#-contato)

## Sobre o Projeto

**FinTrackerAPI** é o backend para uma aplicação de controle financeiro. Ela permite que os usuários gerenciem suas finanças, incluindo carteiras, cartões de crédito e transações, de forma segura e eficiente. 
A FinTrackerAPI permite o gerenciamento de usuários, suas carteiras (contas) e cartões, além de registrar transações entre carteiras. O projeto foi construído utilizando as melhores práticas de desenvolvimento backend, incluindo containerização com Docker, migrações de banco de dados com Alembic e uma suíte de testes automatizados com Pytest.

##  Funcionalidades

-    Autenticação e gerenciamento de usuários.
-    Gerenciamento de carteiras (contas).
-    Gerenciamento de cartões de crédito.
-    Registro e categorização de transações.
-    Paginação automática em endpoints de listagem.
-    Health check para monitoramento da aplicação.

##  Tecnologias Utilizadas

- **Backend:** Python 3.11+, FastAPI
- **Banco de Dados:** PostgreSQL (via Docker)
- **ORM e Migrações:** SQLAlchemy, Alembic
- **Validação de Dados:** Pydantic
- **Containerização:** Docker, Docker Compose
- **Testes:** Pytest
- **Paginação:** fastapi-pagination

## Começando

Siga os passos abaixo para executar a aplicação em seu ambiente local.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Crie o arquivo de ambiente:**
    - Renomeie o arquivo `.env.example` para `.env`.
    - Altere os valores das variáveis de ambiente no arquivo `.env`, se desejar (especialmente as senhas).

3.  **Suba os contêineres com Docker Compose:**
    Este comando irá construir a imagem da API, baixar a imagem do PostgreSQL e iniciar ambos os serviços. As migrações do Alembic serão aplicadas automaticamente.
    ```bash
    docker-compose up --build
    ```

4.  **Acesse a API:**
    - A documentação interativa (Swagger UI) estará disponível em: **http://localhost:8000/docs**
    - O endpoint de health check estará em: **http://localhost:8000/health**

## Executando os Testes

Para garantir a qualidade e a integridade do código, a suíte de testes automatizados pode ser executada com o seguinte comando (requer um ambiente virtual Python com as dependências do `requirements.txt` instaladas):

1) Crie e ative um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate # ou .\venv\Scripts\activate no Windows
```
2) Instale as dependências
```pip install -r requirements.txt```

3) Execute os testes
pytest

### Endpoints Principais

-   `GET /health`: Verifica o status da aplicação.
-   **Recursos da API (sob `/api/v1/`)**:
    -   Endpoints para Usuários
    -   Endpoints para Carteiras
    -   Endpoints para Cartões
    -   Endpoints para Transações

##  Migrações de Banco de Dados

O projeto utiliza o **Alembic** para gerenciar as migrações do esquema do banco de dados.

O script executa automaticamente as migrações pendentes durante a inicialização do container, garantindo que o banco de dados esteja sempre atualizado.

Para criar uma nova migração após alterar os modelos do SQLAlchemy:

1.  Certifique-se de que os containers estejam em execução (`docker-compose up -d`).
2.  Execute o comando do Alembic dentro do container da API (assumindo que o serviço se chama `web` no `docker-compose.yml`):
    ```sh
    docker-compose exec web alembic revision --autogenerate -m
    ```

## 📜 Licença

Este projeto está licenciado sob a Licença MIT
Você é livre para usar, modificar e distribuir este código, com ou sem alterações, respeitando os termos da [Licença MIT](https://opensource.org/licenses/MIT).

## 📫 Contato

[![LinkedIn](https://custom-icon-badges.demolab.com/badge/LinkedIn-0A66C2?logo=linkedin-white&logoColor=fff)](https://www.linkedin.com/in/victor-moreira-4210b9358/)
[![GitHub](https://custom-icon-badges.demolab.com/badge/GitHub-181717?logo=github&logoColor=fff)](https://github.com/StricterBot)
<br><b>Stricter</b><br>
