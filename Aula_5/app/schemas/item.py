from pydantic import BaseModel, EmailStr


class Aluno(BaseModel):
    id: int
    nome: str
    email: str
    curso: str
    matricula: int

    class Config:
        from_attributes = True


class AlunoCreate(BaseModel):
    nome: str
    email: EmailStr
    curso: str


class AlunoUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    curso: str | None = None
