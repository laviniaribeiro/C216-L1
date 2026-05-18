import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.connection import get_connection


@pytest.fixture(scope="session")
def client():
    """Create a test client and ensure startup/shutdown."""
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
async def clean_db(client):
    """Clean the database before each test."""
    conn = await get_connection()
    try:
        await conn.execute("DELETE FROM alunos")
    finally:
        await conn.close()
    yield


class TestAlunos:
    """Test suite for alunos endpoints."""

    @pytest.mark.asyncio
    async def test_listar_alunos_vazio(self, client, clean_db):
        """Test listing alunos when database is empty."""
        response = client.get("/api/v1/alunos")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_criar_aluno_ges(self, client, clean_db):
        """Test creating an aluno in GES course."""
        aluno_data = {
            "nome": "João Silva",
            "email": "joao@example.com",
            "curso": "GES",
        }
        response = client.post("/api/v1/alunos", json=aluno_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "João Silva"
        assert data["email"] == "joao@example.com"
        assert data["curso"] == "GES"
        assert data["matricula"] == 1
        assert "id" in data

    @pytest.mark.asyncio
    async def test_criar_aluno_gec(self, client, clean_db):
        """Test creating an aluno in GEC course."""
        aluno_data = {
            "nome": "Maria Santos",
            "email": "maria@example.com",
            "curso": "GEC",
        }
        response = client.post("/api/v1/alunos", json=aluno_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Maria Santos"
        assert data["email"] == "maria@example.com"
        assert data["curso"] == "GEC"
        assert data["matricula"] == 1
        assert "id" in data

    @pytest.mark.asyncio
    async def test_criar_tres_alunos_ges(self, client, clean_db):
        """Test creating 3 alunos in GES course."""
        alunos_data = [
            {"nome": "Aluno 1 GES", "email": "aluno1@example.com", "curso": "GES"},
            {"nome": "Aluno 2 GES", "email": "aluno2@example.com", "curso": "GES"},
            {"nome": "Aluno 3 GES", "email": "aluno3@example.com", "curso": "GES"},
        ]

        for aluno_data in alunos_data:
            response = client.post("/api/v1/alunos", json=aluno_data)
            assert response.status_code == 200

        # List alunos
        response = client.get("/api/v1/alunos")
        assert response.status_code == 200
        alunos = response.json()
        assert len(alunos) == 3
        for i, aluno in enumerate(alunos):
            assert aluno["nome"] == f"Aluno {i+1} GES"
            assert aluno["matricula"] == i + 1

    @pytest.mark.asyncio
    async def test_criar_tres_alunos_gec(self, client, clean_db):
        """Test creating 3 alunos in GEC course."""
        alunos_data = [
            {"nome": "Aluno 1 GEC", "email": "alunogec1@example.com", "curso": "GEC"},
            {"nome": "Aluno 2 GEC", "email": "alunogec2@example.com", "curso": "GEC"},
            {"nome": "Aluno 3 GEC", "email": "alunogec3@example.com", "curso": "GEC"},
        ]

        for aluno_data in alunos_data:
            response = client.post("/api/v1/alunos", json=aluno_data)
            assert response.status_code == 200

        # List alunos
        response = client.get("/api/v1/alunos")
        assert response.status_code == 200
        alunos = response.json()
        assert len(alunos) == 3
        for i, aluno in enumerate(alunos):
            assert aluno["nome"] == f"Aluno {i+1} GEC"
            assert aluno["matricula"] == i + 1

    @pytest.mark.asyncio
    async def test_listar_alunos_multiplos(self, client, clean_db):
        """Test listing multiple alunos from different courses."""
        # Create alunos
        alunos_data = [
            {"nome": "Aluno 1 GES", "email": "ges1@example.com", "curso": "GES"},
            {"nome": "Aluno 1 GEC", "email": "gec1@example.com", "curso": "GEC"},
            {"nome": "Aluno 2 GES", "email": "ges2@example.com", "curso": "GES"},
        ]

        ids = []
        for aluno_data in alunos_data:
            response = client.post("/api/v1/alunos", json=aluno_data)
            assert response.status_code == 200
            ids.append(response.json()["id"])

        # List alunos
        response = client.get("/api/v1/alunos")
        assert response.status_code == 200
        alunos = response.json()
        assert len(alunos) == 3

    @pytest.mark.asyncio
    async def test_buscar_aluno_por_id(self, client, clean_db):
        """Test finding an aluno by ID."""
        # Create aluno
        aluno_data = {
            "nome": "Teste Busca",
            "email": "busca@example.com",
            "curso": "GES",
        }
        response = client.post("/api/v1/alunos", json=aluno_data)
        aluno_id = response.json()["id"]

        # Search by ID
        response = client.get(f"/api/v1/alunos/{aluno_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == aluno_id
        assert data["nome"] == "Teste Busca"
        assert data["email"] == "busca@example.com"

    @pytest.mark.asyncio
    async def test_buscar_aluno_inexistente(self, client, clean_db):
        """Test finding a non-existent aluno."""
        response = client.get("/api/v1/alunos/9999")
        assert response.status_code == 404
        assert "Aluno não encontrado" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_atualizar_aluno(self, client, clean_db):
        """Test updating an aluno."""
        # Create aluno
        aluno_data = {
            "nome": "Aluno Original",
            "email": "original@example.com",
            "curso": "GES",
        }
        response = client.post("/api/v1/alunos", json=aluno_data)
        aluno_id = response.json()["id"]

        # Update aluno
        updated_data = {
            "nome": "Aluno Atualizado",
            "email": "atualizado@example.com",
            "curso": "GES",
        }
        response = client.patch(f"/api/v1/alunos/{aluno_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Aluno Atualizado"
        assert data["email"] == "atualizado@example.com"

    @pytest.mark.asyncio
    async def test_atualizar_aluno_trocar_curso(self, client, clean_db):
        """Test updating an aluno and changing their course."""
        # Create aluno
        aluno_data = {
            "nome": "Aluno Curso 1",
            "email": "curso1@example.com",
            "curso": "GES",
        }
        response = client.post("/api/v1/alunos", json=aluno_data)
        aluno_id = response.json()["id"]
        assert response.json()["matricula"] == 1

        # Update aluno changing course
        updated_data = {
            "nome": "Aluno Curso 2",
            "email": "curso2@example.com",
            "curso": "GEC",
        }
        response = client.patch(f"/api/v1/alunos/{aluno_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["curso"] == "GEC"
        assert data["matricula"] == 1  # First in GEC

    @pytest.mark.asyncio
    async def test_atualizar_aluno_inexistente(self, client, clean_db):
        """Test updating a non-existent aluno."""
        updated_data = {
            "nome": "Novo Nome",
            "email": "novo@example.com",
            "curso": "GES",
        }
        response = client.patch("/api/v1/alunos/9999", json=updated_data)
        assert response.status_code == 404
        assert "Aluno não encontrado" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_deletar_aluno(self, client, clean_db):
        """Test deleting an aluno."""
        # Create aluno
        aluno_data = {
            "nome": "Aluno Para Deletar",
            "email": "deletar@example.com",
            "curso": "GES",
        }
        response = client.post("/api/v1/alunos", json=aluno_data)
        aluno_id = response.json()["id"]

        # Delete aluno
        response = client.delete(f"/api/v1/alunos/{aluno_id}")
        assert response.status_code == 200
        assert "deletado com sucesso" in response.json()["mensagem"]

        # Verify deletion
        response = client.get(f"/api/v1/alunos/{aluno_id}")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_deletar_aluno_inexistente(self, client, clean_db):
        """Test deleting a non-existent aluno."""
        response = client.delete("/api/v1/alunos/9999")
        assert response.status_code == 404
        assert "Aluno não encontrado" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_criar_aluno_curso_invalido(self, client, clean_db):
        """Test creating an aluno with invalid course."""
        aluno_data = {
            "nome": "Aluno Inválido",
            "email": "invalido@example.com",
            "curso": "INVALID",
        }
        response = client.post("/api/v1/alunos", json=aluno_data)
        assert response.status_code == 400
        assert "Curso deve ser" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_persistencia_dados(self, client, clean_db):
        """Test data persistence - create, list, verify."""
        # Create alunos
        alunos_data = [
            {"nome": "Persistência 1", "email": "pers1@example.com", "curso": "GES"},
            {"nome": "Persistência 2", "email": "pers2@example.com", "curso": "GEC"},
        ]

        for aluno_data in alunos_data:
            response = client.post("/api/v1/alunos", json=aluno_data)
            assert response.status_code == 200

        # List and verify
        response = client.get("/api/v1/alunos")
        assert response.status_code == 200
        alunos = response.json()
        assert len(alunos) == 2
        assert alunos[0]["nome"] == "Persistência 1"
        assert alunos[1]["nome"] == "Persistência 2"
