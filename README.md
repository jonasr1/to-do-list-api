# TodoList

## 📚 Sumário

- [Requisitos](#requisitos)
- [1. Como instalar o Poetry](#1-como-instalar-o-poetry)
- [2. Como instalar e configurar o Redis](#2-como-instalar-e-configurar-o-redis)
- [3. Como executar o projeto](#3-como-executar-o-projeto)
- [Endpoints da API](#endpoints-da-api)
  - [Autenticação e Usuário](#-autenticação-e-usuário-usersautenticacao-e-usuario-users)
  - [Tarefas](#-tarefas-tasks)
  - [Histórico de Tarefas](#-histórico-de-tarefas-task-history)
  - [Exemplos de Requisições no Postman - Autenticação](#-exemplos-de-requisições-no-postman--autenticação)
  - [Exemplos de Requisições no Postman - Tasks](#-exemplos-de-requisições-via-postman---tasks)
  - [Decisões Técnicas do Projeto](#-decisões-técnicas-do-projeto)

## Requisitos  

Antes de rodar o projeto, certifique-se de que os seguintes itens estão instalados:

- [Poetry](https://python-poetry.org/docs/#installation) → Gerenciamento de dependências e ambiente virtual.

- [Redis](https://hub.docker.com/_/redis) → Utilizado para caching e otimização de desempenho da API.

## 1. Como instalar o Poetry

Se você ainda não tem o Poetry instalado, recomenda-se a instalação via curl, que é a forma mais confiável para garantir um ambiente isolado:
  
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Caso prefira, também é possível instalar via pip:

```bash
pip install poetry
```

Após a instalação, você pode verificar se o Poetry foi instalado corretamente com o comando:

```bash
poetry --version
```

## 2. **Como instalar e configurar o Redis**

O Redis é necessário para caching e otimização da API.

### 🔹 **Linux (Ubuntu/Debian)**

```bash
sudo apt update && sudo apt install redis

```

### 🔹 **MacOS (via Homebrew)**

```bash
brew install redis
```

### 🔹 **Windows**

No Windows, recomenda-se usar o **WSL (Windows Subsystem for Linux)** para rodar o Redis.

Caso tenha o Docker instalado, você pode rodar o Redis com:

```bash
docker run --name redis -p 6379:6379 -d redis
```

### 🔹 **Verificar se o Redis está rodando**

Após a instalação, inicie o Redis com:

```bash
redis-server
```

Ou, se estiver rodando no Docker:

```bash
docker ps
```

Para testar a conexão:

```bash
redis-cli ping
```

Se tudo estiver funcionando, o retorno será:
`PONG`

## 3. Como executar o projeto

1. Instalar as dependências do projeto:

Dentro da pasta do projeto, execute o seguinte comando para instalar todas as dependências listadas no arquivo pyproject.toml:

```bash
poetry install
```

O Poetry irá criar um ambiente virtual e instalar todas as dependências listadas no pyproject.toml.

2 Aplicar as migrações do banco de dados:

```bash
poetry run python manage.py migrate
```

3 Ativar o ambiente virtual (opcional):

Embora o Poetry gerencie o ambiente automaticamente ao executar os comandos, você pode ativá-lo manualmente com:

Após instalar as dependências, você pode ativar o ambiente virtual com o comando:

```bash
poetry shell
```
  
Executar o script:
  
Para executar o script, use o comando abaixo para rodar o arquivo Python dentro do ambiente virtual do Poetry:

```bash
poetry run python manage.py runserver
```

Ou, se você tiver configurado o Poetry como interpretador no seu editor, pode simplesmente rodar o script diretamente dentro do editor.

`python manage.py runserver`

Verificar onde o ambiente virtual foi criado:

```bash
poetry env info --path
```

## Endpoints da API

### 👤 Autenticação e Usuário (`/users/`){#autenticacao-e-usuario-users}

|Método|Rota|Descrição|
|---|---|---|
|POST|`/users/register/`|Registro de novo usuário|
|POST|`/users/login/`|Login do usuário (JWT) — retorna access e refresh token|
|POST|`/users/token/refresh/`|Atualiza o token de acesso (JWT) com o refresh token|
|POST|`/users/token/verify/`|Verifica se o token JWT é válido|
|GET|`/users/me/`|Retorna os dados do usuário autenticado|

### 🧾 Tarefas (`/tasks/`)

| Método | Rota                         | Descrição                                                                                         |
| ------ | ---------------------------- | ------------------------------------------------------------------------------------------------- |
| POST   | `/tasks/`                    | Criar uma nova tarefa                                                                             |
| GET    | `/tasks/`                    | Listar tarefas com filtros, ordenação e paginação                                                 |
| GET    | `/tasks/?page_size=n&page=m` | Paginação das tarefas (`n` por página, `m` página)                                                |
| GET    | `/tasks?status={{status}}`   | Filtrar tarefas pelo status usando o parâmetro de consulta 'status' (completed \| pending \| all) |
| PUT    | `/tasks/:id/`                | Atualizar uma tarefa inteira                                                                      |
| PATCH  | `/tasks/:id/`                | Marcar/desmarcar tarefa como concluída                                                            |
| DEL    | `/tasks/:id/`                | Excluir uma tarefa                                                                                |
| GET    | `/tasks/stats/`              | Estatísticas das tarefas do usuário                                                               |
| GET    | `/tasks/metrics/?days=n`     | Tarefas criadas nos últimos `n` dias                                                              |

### Classificação

- Classificar por 'created_at' ou 'title' usando 'ordering':

 ```- GET /tasks?ordering=created_at
- GET /tasks?ordering=-created_at
- GET /tasks?ordering=title
- GET /tasks?ordering=-title
```

### 📖 Histórico de Tarefas (`/task-history/`)

|Método|Rota|Descrição|
|---|---|---|
|GET|`/task-history/`|Lista o histórico de todas as tarefas|
|GET|`/task-history/?task=<id>`|Histórico de uma tarefa específica|

### 🧪 Exemplos de requisições no Postman – Autenticação

#### 🔹 Registrar novo usuário – `POST /users/register/`

```json
{
"username": "{{USERNAME}}",
"password": "{{PASSWORD}}"
}
```

#### 🔹 Atualizar access token – `POST /users/token/refresh/`

```json
{
"refresh": "<refresh_token>"
}
```

🔹 Verificar validade do token – `POST /users/token/verify/`

```json
{
  "token": "<access_token>"
}
```

#### 🔹 Obter dados do usuário autenticado – `GET /users/me/`

```http
GET /users/me/
{Authorization: Bearer <access_token>
```

### 📬 Exemplos de Requisições via Postman - Tasks

### 🔐 Autenticação (Token JWT)

1. Vá na aba **Authorization**.
2. Tipo: **Bearer Token**.
3. Cole seu token JWT no campo `Token`.

 **Observação**: Todos os endpoints (exceto `/register/` e `/login/`) requerem autenticação com **JWT** no cabeçalho:

#### 🔸 Criar uma Tarefa

- **Method:** `POST`

- **URL:** `http://localhost:8000/tasks/`

- **Body (raw → JSON):**

```json
{
  "title": "Estudar Django",
  "description": "Estudar views e serializers"
}
```

#### 🔹 Listar Tarefas

- **Method:** `GET`

- **URL:** `http://localhost:8000/tasks/?status=pending&page_size=5&ordering=-created_at`

#### 🟢 Atualizar Tarefa Inteira

- **Method:** `PUT`

- **URL:** `http://localhost:8000/tasks/<id>/`

- **Body (raw → JSON):**

```json
{
  "title": "Novo título",
  "description": "Nova descrição",
  "is_completed": false
}
```

#### ✅ Marcar como Concluída

- **Method:** `PATCH`

- **URL:** `http://localhost:8000/tasks/<id>/`

- **Body (raw → JSON):**

```json
{
  "is_completed": true
}
```

#### ❌ Excluir Tarefa

- **Method:** `DELETE`

- **URL:** `http://localhost:8000/tasks/<id>/`

---

#### 📊 Ver Estatísticas

- **Method:** `GET`

- **URL:** `http://localhost:8000/tasks/stats/`

---

#### 📈 Tarefas nos Últimos N Dias

- **Method:** `GET`

- **URL:** `http://localhost:8000/tasks/metrics/?days=7`

---

#### 📚 Ver Histórico de Tarefas

- **Method:** `GET`

- **URL:** `http://localhost:8000/task-history/`

---

#### 📘 Histórico de uma Tarefa Específica

- **Method:** `GET`

- **URL:** `http://localhost:8000/task-history/?task=<id>`

## 🧠 Decisões Técnicas do Projeto

### 1. **Framework Utilizado: Django + Django REST Framework**

- **Motivo:** Django é robusto, maduro e permite criação rápida de aplicações web. O Django REST Framework (DRF) oferece suporte completo para criação de APIs RESTful com recursos prontos como autenticação, permissões, serialização e paginação.

- **Benefício:** Permite focar na lógica de negócio, evitando retrabalho com estrutura básica da API.

---

### 2. **Arquitetura do Projeto**

- **Padrão:** Aplicações separadas por responsabilidade (`users`, `tasks`, `core`).

- **Motivo:** Separação de responsabilidades (Separation of Concerns) facilita a manutenção e escalabilidade.

- **Exemplo:**

  - `users`: gerencia autenticação e cadastro.

  - `tasks`: lida com CRUD de tarefas.

  - `core`: configurações e roteamento principal.

---

### 3. **Autenticação com JWT**

- **Motivo:** JWT permite autenticação stateless (sem sessão no servidor), ideal para APIs RESTful.

- **Tecnologia usada:** `djangorestframework-simplejwt`

- **Benefício:** Integração fácil com frontend e aplicativos mobile.

---

### 4. **Filtragem com django-filter**

- **Motivo:** Permite filtros avançados em endpoints, como tarefas concluídas ou pendentes.

- **Exemplo:** `TaskFilter` permite filtrar por `status`, `created_at`, etc.

---

### 5. **Uso de `.env` para variáveis sensíveis**

- **Motivo:** Evita expor segredos no código.

- **Tecnologia usada:** `python-decouple`.
