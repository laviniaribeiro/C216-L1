from app.db.connection import get_connection
from app.schemas.item import Aluno, AlunoCreate, AlunoUpdate

VALID_CURSOS = {"GES", "GEC"}


class AlunoService:
    async def listar(self) -> list[dict]:
        """List all alunos from the database."""
        conn = await get_connection()
        try:
            rows = await conn.fetch("SELECT * FROM alunos ORDER BY id")
            return [dict(row) for row in rows]
        finally:
            await conn.close()

    async def buscar_por_id(self, aluno_id: int) -> dict | None:
        """Find an aluno by ID."""
        conn = await get_connection()
        try:
            row = await conn.fetchrow(
                "SELECT * FROM alunos WHERE id=$1", aluno_id
            )
            return dict(row) if row else None
        finally:
            await conn.close()

    async def criar(self, aluno_data: AlunoCreate) -> dict:
        """Create a new aluno in the database."""
        curso = aluno_data.curso.strip().upper()
        if curso not in VALID_CURSOS:
            raise ValueError(
                f"Curso deve ser um dos valores: {', '.join(sorted(VALID_CURSOS))}"
            )

        conn = await get_connection()
        try:
            # Get the next matricula for this curso
            result = await conn.fetchval(
                "SELECT COALESCE(MAX(matricula), 0) + 1 FROM alunos WHERE curso=$1",
                curso,
            )
            matricula = result

            row = await conn.fetchrow(
                """
                INSERT INTO alunos (nome, email, curso, matricula)
                VALUES ($1, $2, $3, $4)
                RETURNING *
                """,
                aluno_data.nome,
                aluno_data.email,
                curso,
                matricula,
            )
            return dict(row)
        finally:
            await conn.close()

    async def atualizar(self, aluno_id: int, aluno_data: AlunoUpdate) -> dict | None:
        """Update an aluno in the database."""
        conn = await get_connection()
        try:
            # First get the current aluno
            aluno = await conn.fetchrow("SELECT * FROM alunos WHERE id=$1", aluno_id)
            if not aluno:
                return None

            # Prepare fields to update
            nome = aluno_data.nome if aluno_data.nome is not None else aluno["nome"]
            email = aluno_data.email if aluno_data.email is not None else aluno["email"]
            
            if aluno_data.curso is not None:
                curso = aluno_data.curso.strip().upper()
                if curso not in VALID_CURSOS:
                    raise ValueError(
                        f"Curso deve ser um dos valores: {', '.join(sorted(VALID_CURSOS))}"
                    )
            else:
                curso = aluno["curso"]

            # If curso changed, get new matricula
            if curso != aluno["curso"]:
                result = await conn.fetchval(
                    "SELECT COALESCE(MAX(matricula), 0) + 1 FROM alunos WHERE curso=$1",
                    curso,
                )
                matricula = result
            else:
                matricula = aluno["matricula"]

            row = await conn.fetchrow(
                """
                UPDATE alunos
                SET nome=$1, email=$2, curso=$3, matricula=$4
                WHERE id=$5
                RETURNING *
                """,
                nome,
                email,
                curso,
                matricula,
                aluno_id,
            )
            return dict(row) if row else None
        finally:
            await conn.close()

    async def deletar(self, aluno_id: int) -> bool:
        """Delete an aluno from the database."""
        conn = await get_connection()
        try:
            result = await conn.execute("DELETE FROM alunos WHERE id=$1", aluno_id)
            return result == "DELETE 1"
        finally:
            await conn.close()
