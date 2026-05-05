from fastapi import APIRouter, HTTPException

from app.schemas.item import Aluno, AlunoCreate, AlunoUpdate
from app.services.item_service import AlunoService

router = APIRouter()
service = AlunoService()

@router.get("/alunos", response_model=list[Aluno])
def listar_alunos():
    return service.listar()

@router.get("/alunos/{aluno_id}", response_model=Aluno)
def buscar_aluno(aluno_id: str):
    aluno = service.buscar_por_id(aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@router.post("/alunos", response_model=Aluno)
def criar_aluno(aluno: AlunoCreate):
    try:
        return service.criar(aluno)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

@router.patch("/alunos/{aluno_id}", response_model=Aluno)
def atualizar_aluno(aluno_id: str, aluno: AlunoUpdate):
    try:
        atualizado = service.atualizar(aluno_id, aluno)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    if not atualizado:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return atualizado

@router.delete("/alunos/{aluno_id}")
def deletar_aluno(aluno_id: str):
    sucesso = service.deletar(aluno_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return {"mensagem": "Aluno deletado com sucesso"}

@router.delete("/alunos")
def resetar_alunos():
    service.resetar()
    return {"mensagem": "Lista de alunos resetada"}
