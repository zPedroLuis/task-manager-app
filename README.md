# Task Manager App

Aplicação web de gerenciamento de tarefas (To-Do List) com:

- autenticação de usuário (cadastro e login)
- CRUD de tarefas
- categorias para organização
- compartilhamento de tarefas
- filtro e paginação
- integração com API externa
- testes no back-end com `pytest`
- teste E2E inicial com `Selenium`
- execução com Docker e Docker Compose

## Arquitetura

### Backend

- Django + Django REST Framework
- JWT com `djangorestframework-simplejwt`
- Banco PostgreSQL
- App `accounts`: registro/login/perfil
- App `tasks`: categorias e tarefas
- App `integrations`: consumo de API externa

### Frontend

- React (Vite)
- `axios` para integração com API
- interface com autenticação e tela de tarefas

### API Externa

- Serviço FastAPI separado (`external_api`)
- Endpoint `/tips` para sugerir título de tarefas por categoria

## Decisões de design

- **KISS**: estrutura simples com apps pequenos e responsabilidades claras.
- **DRY**: serialização e validações centralizadas em serializers.
- **SOLID**:
	- responsabilidade única em `views`, `serializers`, `models`.
	- permissões encapsuladas em classe própria (`IsOwnerOrSharedReadOnly`).

## Requisitos atendidos

- React
- Docker e Docker Compose
- Django REST Framework
- Testes unitários no backend com pytest
- Teste E2E inicial com Selenium
- CI/CD com GitHub Actions

## Como rodar com Docker

Pré-requisito: Docker e Docker Compose instalados.

1. Subir ambiente:

```bash
docker compose up --build
```

2. Acessos:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api
- Admin Django: http://localhost:8000/admin
- External API: http://localhost:8001

## Endpoints principais

### Auth

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`
- `GET /api/auth/me/`

### Categorias

- `GET /api/categories/`
- `POST /api/categories/`
- `PUT/PATCH/DELETE /api/categories/{id}/`

### Tarefas

- `GET /api/tasks/`
- `POST /api/tasks/`
- `PUT/PATCH/DELETE /api/tasks/{id}/`

Filtros:

- `?completed=true|false`
- `?category={id}`
- `?search=texto`

Paginação:

- padrão DRF (`count`, `next`, `previous`, `results`)

### Integração externa

- `GET /api/integrations/suggested-task-title/?category=trabalho`

## Rodando testes

### Backend (pytest)

```bash
docker compose exec backend pytest
```

### Frontend E2E (Selenium)

Arquivo: `frontend/selenium/test_login.py`

Esse teste exige um Selenium Hub/Server disponível em `SELENIUM_URL`.

Exemplo:

```bash
SELENIUM_URL=http://localhost:4444/wd/hub pytest frontend/selenium
```

## CI/CD

Pipeline configurado em:

- `.github/workflows/ci.yml`

Jobs:

- testes de backend
- build de frontend