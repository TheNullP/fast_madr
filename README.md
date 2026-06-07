# MADR - Meu Acervo Digital de Romances

O objetivo principal deste projeto é criar uma API para gerenciar livros e seus autores em um contexto simplificado. A API vai permitir o cadastro, consulta, atualização e exclusão de livros, assim como o gerenciamento de usuários e controle de acesso.

---

### 🏗️ Estrutura do Projeto

O projeto está dividido em três principais seções:

* **Contas:** Gerenciamento de contas de usuários e autenticação via API.
* **Livros:** Gerenciamento do acervo de livros (CRUD).
* **Autores:** Gerenciamento dos autores (CRUD).

---

### 💻 Tecnologias Utilizadas

* **FastAPI:** Framework web para construção da API.
* **SQLAlchemy:** ORM para o gerenciamento do banco de dados.
* **PostgreSQL:** Banco de dados relacional.
* **JWT:** Padrão utilizado para a autenticação segura.
* **Docker & Docker Compose:** Containerização e orquestração da aplicação.
* **Cloudinary:** Serviço de nuvem para armazenamento e otimização de imagens e PDFs.

---

### 🚀 Projeto em Produção (VPS Autogerenciada)

A aplicação está atualmente em produção, hospedada em um servidor privado virtual (VPS) com orquestração via Docker e roteamento seguro (HTTPS) gerido dinamicamente.

Você pode acessar a versão mais recente e interagir com os *endpoints* através dos links abaixo:

* **Acesso à Aplicação:** [https://madr-thenullp.duckdns.org/](https://madr-thenullp.duckdns.org/)
* **Documentação Interativa (Swagger UI):** [https://madr-thenullp.duckdns.org/docs](https://madr-thenullp.duckdns.org/docs)

---

### 🛠️ Instalação e Execução (Ambiente Local)

#### Pré-requisitos

* Docker e Docker Compose
* Python 3.10+

#### Passos para rodar o projeto

1.  **Clone o repositório:**
```bash
git clone [https://github.com/TheNullP/fast_madr.git](https://github.com/TheNullP/fast_madr.git)
cd fast_madr
```

2.  **Instale as dependências:**
```bash
poetry install
```

3.  **Configure as variáveis de ambiente:**
    Crie uma cópia do arquivo `.env.example` e renomeie para `.env`, preenchendo com as suas credenciais de desenvolvimento.

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

### 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo `LICENSE` para mais detalhes.
