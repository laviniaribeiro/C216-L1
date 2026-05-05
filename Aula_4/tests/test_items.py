from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def setup_function():
    client.delete("/api/v1/alunos")


def criar_aluno(nome: str, email: str, curso: str) -> dict:
    response = client.post(
        "/api/v1/alunos",
        json={"nome": nome, "email": email, "curso": curso}
    )
    assert response.status_code == 200
    return response.json()


def test_criar_alunos_por_curso():
    a1 = criar_aluno("Ana", "ana@exemplo.com", "GES")
    a2 = criar_aluno("Beto", "beto@exemplo.com", "GES")
    a3 = criar_aluno("Carla", "carla@exemplo.com", "GES")
    a4 = criar_aluno("Diego", "diego@exemplo.com", "GEC")
    a5 = criar_aluno("Eva", "eva@exemplo.com", "GEC")
    a6 = criar_aluno("Fábio", "fabio@exemplo.com", "GEC")

    assert a1["id"] == "GES1"
    assert a2["id"] == "GES2"
    assert a3["id"] == "GES3"
    assert a4["id"] == "GEC1"
    assert a5["id"] == "GEC2"
    assert a6["id"] == "GEC3"


def test_listar_alunos():
    criar_aluno("Ana", "ana@exemplo.com", "GES")
    criar_aluno("Beto", "beto@exemplo.com", "GEC")

    response = client.get("/api/v1/alunos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_buscar_aluno_por_id():
    aluno = criar_aluno("Carla", "carla@exemplo.com", "GES")

    response = client.get(f"/api/v1/alunos/{aluno['id']}")
    assert response.status_code == 200
    assert response.json()["email"] == "carla@exemplo.com"


def test_atualizar_aluno():
    aluno = criar_aluno("Diego", "diego@exemplo.com", "GEC")

    response = client.patch(
        f"/api/v1/alunos/{aluno['id']}",
        json={"nome": "Diego Silva", "email": "diego.silva@exemplo.com"}
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Diego Silva"
    assert response.json()["email"] == "diego.silva@exemplo.com"


def test_deletar_aluno_e_nao_reutilizar_id():
    aluno1 = criar_aluno("Eva", "eva@exemplo.com", "GES")
    criar_aluno("Bruno", "bruno@exemplo.com", "GES")

    response = client.delete(f"/api/v1/alunos/{aluno1['id']}")
    assert response.status_code == 200

    novo_aluno = criar_aluno("Fábio", "fabio@exemplo.com", "GES")
    assert novo_aluno["id"] != aluno1["id"]
    assert novo_aluno["id"].startswith("GES")


def test_resetar_alunos():
    criar_aluno("Gabriela", "gabriela@exemplo.com", "GEC")

    response = client.delete("/api/v1/alunos")
    assert response.status_code == 200
    assert response.json()["mensagem"] == "Lista de alunos resetada"

    response = client.get("/api/v1/alunos")
    assert response.status_code == 200
    assert response.json() == []


def test_post_curso_invalido():
    response = client.post(
        "/api/v1/alunos",
        json={"nome": "João", "email": "joao@exemplo.com", "curso": "INVALID"}
    )
    assert response.status_code == 400
    assert "Curso deve ser um dos valores" in response.json()["detail"]


def test_get_aluno_por_id_inexistente():
    response = client.get("/api/v1/alunos/GES999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Aluno não encontrado"


def test_patch_aluno_inexistente():
    response = client.patch(
        "/api/v1/alunos/GES999",
        json={"nome": "Novo Nome"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Aluno não encontrado"


def test_patch_curso_invalido():
    aluno = criar_aluno("Maria", "maria@exemplo.com", "GES")
    response = client.patch(
        f"/api/v1/alunos/{aluno['id']}",
        json={"curso": "INVALID"}
    )
    assert response.status_code == 400
    assert "Curso deve ser um dos valores" in response.json()["detail"]


def test_delete_aluno_inexistente():
    response = client.delete("/api/v1/alunos/GES999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Aluno não encontrado"
