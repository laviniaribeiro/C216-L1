from typing import Optional

from pydantic import BaseModel, EmailStr

class Aluno(BaseModel):
    id: str
    nome: str
    email: EmailStr
    curso: str
    matricula: int

class AlunoCreate(BaseModel):
    nome: str
    email: EmailStr
    curso: str

class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    curso: Optional[str] = None
