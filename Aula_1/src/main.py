from services import create_aluno, read_alunos, update_aluno, delete_aluno


def exibir_menu():
    print("\n===== Sistema de Cadastro de Alunos =====")
    print("1 - Cadastrar aluno")
    print("2 - Listar alunos")
    print("3 - Atualizar aluno")
    print("4 - Excluir aluno")
    print("0 - Sair")


def main():
    alunos = []
    counters = {}

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            create_aluno(alunos, counters)
        elif opcao == "2":
            read_alunos(alunos)
        elif opcao == "3":
            update_aluno(alunos)
        elif opcao == "4":
            delete_aluno(alunos)
        elif opcao == "0":
            print("Saindo. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
