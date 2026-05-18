from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routes.item_routes import router as aluno_router
from app.middlewares.logging import log_requests
from app.middlewares.custom_header import add_custom_header
from app.db.connection import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for app startup and shutdown."""
    # Startup
    await init_db()
    yield
    # Shutdown
    print("🛑 Shutting down...")


app = FastAPI(
    title="API de Alunos com PostgreSQL",
    description="API para estudo de persistência com PostgreSQL e asyncpg",
    version="1.0.0",
    lifespan=lifespan,
)

app.middleware("http")(log_requests)
app.middleware("http")(add_custom_header)

app.include_router(aluno_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"mensagem": "API funcionando 🚀"}
