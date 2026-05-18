from fastapi import APIRouter, HTTPException

from app.schemas.item import Aluno, AlunoCreate, AlunoUpdate
from app.services.item_service import AlunoService

router = APIRouter()
service = AlunoService()


@router.get("/alunos", response_model=list[Aluno])
async def listar_alunos():
    """List all alunos."""
    alunos = await service.listar()
    return alunos


@router.get("/alunos/{aluno_id}", response_model=Aluno)
async def buscar_aluno(aluno_id: int):
    """Get an aluno by ID."""
    aluno = await service.buscar_por_id(aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno


@router.post("/alunos", response_model=Aluno)
async def criar_aluno(aluno: AlunoCreate):
    """Create a new aluno."""
    try:
        return await service.criar(aluno)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.patch("/alunos/{aluno_id}", response_model=Aluno)
async def atualizar_aluno(aluno_id: int, aluno: AlunoUpdate):
    """Update an aluno."""
    try:
        atualizado = await service.atualizar(aluno_id, aluno)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    if not atualizado:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return atualizado


@router.delete("/alunos/{aluno_id}")
async def deletar_aluno(aluno_id: int):
    """Delete an aluno."""
    sucesso = await service.deletar(aluno_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return {"mensagem": "Aluno deletado com sucesso"}
