import asyncpg
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/alunos_db"
)

async def get_connection():
    """Get a connection to the database."""
    return await asyncpg.connect(DATABASE_URL)

async def init_db():
    """Initialize the database with the schema."""
    conn = await get_connection()
    try:
        # Read and execute init.sql
        script_path = os.path.join(os.path.dirname(__file__), "init.sql")
        with open(script_path, "r") as f:
            sql_script = f.read()
        
        await conn.execute(sql_script)
        print("✅ Database initialized successfully!")
    finally:
        await conn.close()
