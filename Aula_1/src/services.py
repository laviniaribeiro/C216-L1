def generate_matricula(curso: str, counters: dict) -> str:
    curso_abv = curso.strip().upper()
    if not curso_abv:
        raise ValueError("Curso não pode ser vazio")

    if curso_abv not in counters:
        counters[curso_abv] = 0

    counters[curso_abv] += 1
    return f"{curso_abv}{counters[curso_abv]}"


def create_aluno(alunos: list, counters: dict):
    nome = input("Digite o nome do aluno: ").strip()
    if not nome:
        print("Nome não pode ser vazio.")
        return

    email = input("Digite o email do aluno: ").strip()
    if not email:
        print("Email não pode ser vazio.")
        return

    curso = input("Digite o curso do aluno (GES/GEC/GET/GEP/etc.): ").strip().upper()
    if not curso:
        print("Curso não pode ser vazio.")
        return

    matricula = generate_matricula(curso, counters)
    aluno = {
        "matricula": matricula,
        "nome": nome,
        "email": email,
        "curso": curso
    }

    alunos.append(aluno)
    print(f"Aluno cadastrado com sucesso! Matrícula: {matricula}")


def read_alunos(alunos: list):
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return

    print("\nLista de alunos cadastrados:")
    for aluno in alunos:
        print(f"Matrícula: {aluno['matricula']}")
        print(f"  Nome: {aluno['nome']}")
        print(f"  Email: {aluno['email']}")
        print(f"  Curso: {aluno['curso']}")
        print("-" * 30)


def find_aluno_by_matricula(alunos: list, matricula: str) -> dict:
    for aluno in alunos:
        if aluno["matricula"].upper() == matricula.upper():
            return aluno
    return None


def update_aluno(alunos: list):
    if not alunos:
        print("Nenhum aluno cadastrado para atualizar.")
        return

    matricula = input("Digite a matrícula do aluno a atualizar: ").strip()
    aluno = find_aluno_by_matricula(alunos, matricula)

    if aluno is None:
        print("Aluno não encontrado.")
        return

    novo_nome = input(f"Digite o novo nome (ou ENTER para manter '{aluno['nome']}'): ").strip()
    if novo_nome:
        aluno['nome'] = novo_nome

    novo_email = input(f"Digite o novo email (ou ENTER para manter '{aluno['email']}'): ").strip()
    if novo_email:
        aluno['email'] = novo_email

    novo_curso = input(f"Digite o novo curso (ou ENTER para manter '{aluno['curso']}'): ").strip().upper()
    if novo_curso:
        aluno['curso'] = novo_curso

    print(f"Aluno {aluno['matricula']} atualizado com sucesso.")


def delete_aluno(alunos: list):
    if not alunos:
        print("Nenhum aluno cadastrado para remover.")
        return

    matricula = input("Digite a matrícula do aluno a remover: ").strip()
    aluno = find_aluno_by_matricula(alunos, matricula)

    if aluno is None:
        print("Aluno não encontrado.")
        return

    alunos.remove(aluno)
    print(f"Aluno {matricula} removido com sucesso.")
