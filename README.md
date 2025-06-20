# MADR - Meu Acervo Digital de Romances

O objetivo principal deste projeto é criar uma API para gerenciar livros e seus autores em um contexto simplificado. A API vai permitir o cadastro, consulta, atualização e exclusão de livros, assim como o gerenciamento de usuários e controle de acesso.

---

### Estrutura do Projeto

O projeto está dividido em três principais seções:

* **Contas:** Gerenciamento de contas de usuários e autenticação via API.
* **Livros:** Gerenciamento do acervo de livros (CRUD).
* **Autores:** Gerenciamento dos autores (CRUD).

---

### Tecnologias Utilizadas

* **FastAPI:** Framework web para construção da API.
* **SQLAlchemy:** ORM para o gerenciamento do banco de dados.
* **PostgreSQL** (ou qualquer banco de dados relacional).
* **JWT** para autenticação.
* **Docker:** Para containerizar a aplicação.
* **Cloudinary:** Serviço de nuvem para armazenamento e otimização de imagens e PDFs.


---

### Instalação e Execução (Local)

#### Pré-requisitos

* Docker
* Python 3.10+

#### Passos para rodar o projeto

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/TheNullP/fast_madr.git
    cd fast_madr
    ```

2.  **Instale as dependências:**
    ```bash
    poetry install
    ```

3.  **Configure as variáveis de ambiente** no arquivo `.env` (exemplo fornecido no `.env.example`).

4.  **Execute as migrações de banco de dados:**
    ```bash
    alembic upgrade head
    ```

5.  **Inicie a aplicação com o Docker:**
    ```bash
    docker-compose up
    ```

6.  **Acesse a API no navegador (localmente):**
    * **Documentação interativa (Swagger UI):** `http://localhost:8000/docs`
    * **OpenAPI schema:** `http://localhost:8000/openapi.json`

---

### Projeto em Produção (Fly.io)

Você pode acessar a versão mais recente do projeto implantada no Fly.io, bem como sua documentação interativa:

* **Acesso à Aplicação:** [https://fast-madr.fly.dev/](https://fast-madr.fly.dev/)
* **Documentação Interativa (Swagger UI):** [https://fast-madr.fly.dev/docs](https://fast-madr.fly.dev/docs)

---

### Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo `LICENSE` para mais detalhes.
