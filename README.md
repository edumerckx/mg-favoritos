# mg-favoritos

API _restful_ para gestão de produtos favoritos de clientes. Possui CRUD de clientes (_customers_), inserção/listagem/deleção de favoritos (_favorites_) autenticação com **jwt**.
Os dados de produtos são obtidos através da [fakestoreapi](https://fakestoreapi.com/)

## Tecnologias
- [Python 3.12+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Docker](https://www.docker.com/)
- [Poetry](https://python-poetry.org/) 
- [Pytest](https://docs.pytest.org/)


## Como executar a aplicação

Este projeto utiliza **fastapi**, um framework web moderno de alta performance. Uma de suas _features_ é fornecer documentação baseada no padrão [OpenAPI](https://github.com/OAI/OpenAPI-Specification), e quando a aplicação estiver _rodando_ é possível acessar o **swagger** no endereço [/docs](http://localhost:8000/docs)
A aplicação pode ser executada em container ou localmente conforme instruções abaixo.

#### Docker-compose

Para utilizar o _docker-compose_ garanta que o **docker** esteja instalado.
No terminal, executar:
```sh
docker-compose up --build
```

#### Localmente

Para executar localmente é necessário que o ambiente tenha:
- **python** 3.12+ instalado
- **poetry** instalado - com ele é criado o 'ambiente virtual' e instaladas as dependências
- um banco de dados executando (de preferência **postgres**) - caso não tenha ou opte pela praticidade poderá ser utilizado _sqlite_
- variáveis de ambiente configuradas (arquivo **.env**) - no projeto tem um [arquivo de exemplo](.env-example) e no [arquivo docker-compose](docker-compose.yml) também tem essas variáveis configuradas

Com os pré-requisitos atendidos executar os comandos:
```sh
# baixa o fonte
git clone git@github.com:edumerckx/mg-favoritos.git

# acessa o diretório do projeto
cd mg-favoritos

# instala dependências
poetry install

# ativa ambiente virutal
poetry shell

# executa migrations no bd
alembic upgrade head

# executa apliação no modo dev
task dev
```

## Como funciona

Nas áreas logadas, o cliente só pode visualizar/editar/deletar os próprios dados.

### Endpoints:
- Não é necessária autenticação
  - **POST /customers/** - cria cliente
  - **POST /auth/token**  - login e geração de access-token
- Necessitam autenticação - _access-token_
  - **GET /customers/{id}**  - recupera dados do cliente
  - **PUT /customers/{id}**  - atualiza dados do cliente
  - **DELETE /customers/{id}** - deleta cliente
  - **GET /favorites**  - lista favoritos 
  - **POST /favorites**  - adiciona favorito 
  - **DELETE /favorites/{id}** - deleta favorito 
  - **POST /auth/refresh_token**  - atualiza access-token



## Checklist
- [x] API
- [x] modelagem de dados (_mg_favoritos/models.py_)
- [x] validação - schemas para request/response (_mg_favoritos/schemas/_) 
- [x] documentação
- [x] autenticação jws