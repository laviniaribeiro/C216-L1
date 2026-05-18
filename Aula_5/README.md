# Aula 5 - Persistência com PostgreSQL

Nesta prática, evoluímos a API de alunos desenvolvida na Aula 4, substituindo o armazenamento em memória por **persistência real utilizando PostgreSQL**.

## 📋 Objetivos

- ✅ Integrar FastAPI com PostgreSQL
- ✅ Utilizar `asyncpg` para acesso assíncrono ao banco
- ✅ Persistir dados de forma real
- ✅ Manter organização do projeto (arquitetura em camadas)
- ✅ Executar API + banco com docker-compose
- ✅ Testar endpoints com TestClient

## 🗂️ Estrutura do Projeto

```
Aula_5/
├── app/
│   ├── db/
│   │   ├── connection.py       # Conexão com PostgreSQL via asyncpg
│   │   ├── init.sql           # Script de inicialização do banco
│   │   └── __init__.py
│   ├── middlewares/
│   │   ├── logging.py          # Middleware de logs
│   │   ├── custom_header.py    # Middleware de header customizado
│   │   └── __init__.py
│   ├── routes/
│   │   ├── aluno_routes.py     # Endpoints da API
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── aluno.py            # Schemas Pydantic
│   │   └── __init__.py
│   ├── services/
│   │   ├── aluno_service.py    # Lógica de negócio (CRUD)
│   │   └── __init__.py
│   ├── main.py                 # Aplicação FastAPI
│   └── __init__.py
├── tests/
│   ├── test_alunos.py          # Testes automatizados
│   └── __init__.py
├── img/                        # Pasta para screenshots
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
└── README.md
```

## 🚀 Como Executar

### Com Docker Compose

```bash
# Subir a API e o banco de dados
docker compose up --build

# Em outro terminal, executar os testes
docker compose run tests

# Parar os serviços
docker compose down
```

### Localmente (com PostgreSQL rodando)

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar a API
uvicorn app.main:app --reload

# Executar os testes (em outro terminal)
pytest
```

## 📊 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Verifica se a API está funcionando |
| GET | `/api/v1/alunos` | Lista todos os alunos |
| GET | `/api/v1/alunos/{id}` | Busca aluno por ID |
| POST | `/api/v1/alunos` | Cria novo aluno |
| PATCH | `/api/v1/alunos/{id}` | Atualiza aluno |
| DELETE | `/api/v1/alunos/{id}` | Deleta aluno |

## 📝 Exemplo de Uso

### Criar aluno
```bash
curl -X POST http://localhost:8000/api/v1/alunos \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@example.com",
    "curso": "GES"
  }'
```

### Listar alunos
```bash
curl http://localhost:8000/api/v1/alunos
```

### Buscar por ID
```bash
curl http://localhost:8000/api/v1/alunos/1
```

### Atualizar aluno
```bash
curl -X PATCH http://localhost:8000/api/v1/alunos/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva Santos",
    "email": "joao.silva@example.com",
    "curso": "GES"
  }'
```

### Deletar aluno
```bash
curl -X DELETE http://localhost:8000/api/v1/alunos/1
```

## 🧪 Testes

Os testes cobrem:

- ✅ Criar 3 alunos por curso (GES e GEC)
- ✅ Listar alunos
- ✅ Buscar por ID
- ✅ Atualizar dados
- ✅ Deletar alunos
- ✅ Validação de persistência
- ✅ Tratamento de erros (aluno não encontrado, curso inválido, etc)

### Executar testes com cobertura
```bash
pytest --cov=app
```

## 🔑 Conceitos Principais

### Persistência com PostgreSQL
- Banco de dados relacional para armazenamento durável
- Tabela `alunos` com colunas: id, nome, email, curso, matricula

### Async com asyncpg
- Acesso assíncrono ao banco de dados
- Operações não-bloqueantes
- Melhor performance e escalabilidade

### Arquitetura em Camadas
- **Routes**: Endpoints da API
- **Services**: Lógica de negócio
- **Schemas**: Validação de dados com Pydantic
- **DB**: Conexão e operações do banco

### Middlewares
- **Logging**: Registra todas as requisições e respostas
- **Custom Header**: Adiciona versão da API às respostas

## 📦 Dependências

```
fastapi>=0.110.0
uvicorn[standard]>=0.23.0
pydantic>=2.8.0
pydantic[email]>=2.8.0
pytest>=8.0.0
httpx>=0.28.0,<0.29.0
asyncpg>=0.30.0
email-validator>=1.5.0
```

## 🐳 Docker Compose

O arquivo `docker-compose.yml` contém:

1. **db**: Serviço PostgreSQL 16 (Alpine)
   - Usuário: postgres
   - Senha: postgres
   - Database: alunos_db
   - Volume persistente: postgres_data

2. **web**: Serviço da API
   - Build a partir do Dockerfile
   - Porta: 8000
   - Recarregamento automático (--reload)
   - Depende do banco estar saudável

3. **tests**: Serviço de testes
   - Executa pytest automaticamente
   - Depende do banco estar saudável

## 📸 Screenshots

Resultados dos testes e logs estão na pasta `img/`.

---

**Desenvolvido com ❤️ para C216**
