# MADR - Meu Acervo Digital de Romances

O objetivo principal deste projeto é criar uma API para gerenciar livros e seus autores (romancistas) em um contexto simplificado. A API vai permitir o cadastro, consulta, atualização e exclusão de livros, assim como o gerenciamento de usuários e controle de acesso.

## Estrutura do Projeto

O projeto está dividido em três principais seções:

- **Contas**: Gerenciamento de contas de usuários e autenticação via API.
- **Livros**: Gerenciamento do acervo de livros (CRUD).
- **Romancistas**: Gerenciamento dos autores (CRUD).

## Tecnologias Utilizadas

- **FastAPI**: Framework web para construção da API.
- **SQLAlchemy**: ORM para o gerenciamento do banco de dados.
- **PostgreSQL** (ou qualquer banco de dados relacional).
- **JWT** para autenticação.
- **Docker**: Para containerizar a aplicação.

## Instalação e Execução

### Pré-requisitos

- [Docker](https://www.docker.com/get-started)
- [Python 3.10+](https://www.python.org/downloads/)

### Passos para rodar o projeto

1. Clone o repositório:

    ```bash
    git clone https://github.com/Mfreitas0/fast_madr.git
    cd madr
    ```

2. Instale as dependências:

    ```bash
    poetry install 
    ```

3. Configure as variáveis de ambiente no arquivo `.env` (exemplo fornecido no `.env.example`).

4. Execute as migrações de banco de dados:

    ```bash
    alembic upgrade head
    ```

5. Inicie a aplicação com o Docker:

    ```bash
    docker-compose up
    ```

6. Acesse a API no navegador:

   - Documentação interativa (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)
   - OpenAPI schema: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)


## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
