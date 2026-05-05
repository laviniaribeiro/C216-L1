from typing import List

from app.schemas.item import Aluno, AlunoCreate, AlunoUpdate

VALID_CURSOS = {"GES", "GEC"}

class AlunoService:
    def __init__(self):
        self._alunos: List[Aluno] = []
        self._counters = {curso: 0 for curso in VALID_CURSOS}

    def listar(self) -> List[Aluno]:
        return self._alunos

    def buscar_por_id(self, aluno_id: str) -> Aluno | None:
        for aluno in self._alunos:
            if aluno.id == aluno_id:
                return aluno
        return None

    def criar(self, aluno_data: AlunoCreate) -> Aluno:
        curso = aluno_data.curso.strip().upper()
        if curso not in VALID_CURSOS:
            raise ValueError(f"Curso deve ser um dos valores: {', '.join(sorted(VALID_CURSOS))}")

        self._counters[curso] += 1
        matricula = self._counters[curso]
        novo_id = f"{curso}{matricula}"

        novo_aluno = Aluno(
            id=novo_id,
            nome=aluno_data.nome,
            email=aluno_data.email,
            curso=curso,
            matricula=matricula
        )
        self._alunos.append(novo_aluno)
        return novo_aluno

    def atualizar(self, aluno_id: str, aluno_data: AlunoUpdate) -> Aluno | None:
        aluno = self.buscar_por_id(aluno_id)
        if not aluno:
            return None

        if aluno_data.nome is not None:
            aluno.nome = aluno_data.nome
        if aluno_data.email is not None:
            aluno.email = aluno_data.email
        if aluno_data.curso is not None:
            curso = aluno_data.curso.strip().upper()
            if curso not in VALID_CURSOS:
                raise ValueError(f"Curso deve ser um dos valores: {', '.join(sorted(VALID_CURSOS))}")
            if curso != aluno.curso:
                self._counters[curso] += 1
                aluno.curso = curso
                aluno.matricula = self._counters[curso]
                aluno.id = f"{curso}{aluno.matricula}"

        return aluno

    def deletar(self, aluno_id: str) -> bool:
        aluno = self.buscar_por_id(aluno_id)
        if aluno:
            self._alunos.remove(aluno)
            return True
        return False

    def resetar(self) -> None:
        self._alunos.clear()
