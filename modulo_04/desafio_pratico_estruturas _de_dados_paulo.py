
def print_header(title):
    """Imprime um cabeçalho padronizado."""
    print("\n" + "="*40)
    print(f"   {title.upper()}")
    print("="*40)

def atividade_lista_compras():
    """Atividade 2.1: Gerenciador de Lista de Compras."""
    print_header("ATIVIDADE 1: LISTA DE COMPRAS")
    lista = []
    
    opcoes = {
        '1': lambda: lista.append(input("Item a adicionar: ")),
        '2': lambda: (item := input("Item a remover: "), lista.remove(item) if item in lista else print(f"'{item}' não está na lista.")),
        '3': lambda: [print(f"{i+1}. {item}") for i, item in enumerate(lista)] if lista else print("(Lista vazia)"),
    }

    while True:
        print("\n1: Adicionar | 2: Remover | 3: Ver Lista | 4: Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '4':
            break
        
        funcao = opcoes.get(escolha)
        if funcao:
            funcao()
        else:
            print("Opção inválida.")

def atividade_dicionario_aluno():
    """Atividade 2.2: Armazena dados de aluno em dicionário e exibe."""
    print_header("ATIVIDADE 2: DICIONÁRIO DE ALUNO")
    aluno = {"nome": "Ana Silva", "idade": 21, "curso": "Engenharia", "notas": [9.5, 8.0, 10.0]}
    
    print(f"Nome: {aluno['nome']}\nIdade: {aluno['idade']} anos\nCurso: {aluno['curso']}")
    print("Notas:", ", ".join(map(str, aluno['notas'])))

def atividade_pares_impares():
    """Atividade 2.3: Percorre um conjunto e exibe pares e ímpares."""
    print_header("ATIVIDADE 3: NÚMEROS PARES E ÍMPARES")
    numeros = {1, 5, 10, 23, 44, 56, 77, 89, 90, 100, 3}
    
    # List Comprehension para máxima concisão
    pares = sorted([num for num in numeros if num % 2 == 0])
    impares = sorted([num for num in numeros if num % 2 != 0])

    print(f"Números: {numeros}\nPares: {pares}\nÍmpares: {impares}")

def desafio_agenda_contatos():
    """Desafio Extra 2: Sistema de agenda de contatos."""
    print_header("DESAFIO EXTRA: AGENDA DE CONTATOS")
    agenda = {"Marcos": "11-99999-8888", "Carla": "21-98765-4321"}
    
    while True:
        print("\n1: Adicionar | 2: Remover | 3: Buscar | 4: Listar | 5: Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome, tel = input("Nome: "), input("Telefone: ")
            if nome not in agenda: agenda[nome] = tel; print(f"'{nome}' adicionado.")
            else: print(f"'{nome}' já existe.")
        elif escolha == '2':
            nome = input("Nome para remover: ")
            if nome in agenda: del agenda[nome]; print(f"'{nome}' removido.")
            else: print(f"'{nome}' não encontrado.")
        elif escolha == '3':
            nome = input("Nome para buscar: ")
            tel = agenda.get(nome)
            print(f"Telefone: {tel}" if tel else f"'{nome}' não encontrado.")
        elif escolha == '4':
            [print(f"Nome: {n} | Tel: {t}") for n, t in agenda.items()] if agenda else print("(Agenda vazia)")
        elif escolha == '5':
            break
        else:
            print("Opção inválida.")


def main():
    atividades = {
        '1': atividade_lista_compras,
        '2': atividade_dicionario_aluno,
        '3': atividade_pares_impares,
        '4': desafio_agenda_contatos,
    }
    while True:
        print_header("MENU PRINCIPAL - BLOCO 2")
        print("1: Lista de Compras | 2: Dicionário Aluno | 3: Pares/Ímpares | 4: Agenda Contatos\n0: Sair")
        escolha = input("\nQual atividade? (0-4): ")
        
        if escolha == '0':
            print("Programa finalizado. Até logo!")
            break
        
        funcao = atividades.get(escolha)
        if funcao:
            funcao()
            input("\nPressione Enter para voltar ao menu...")
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()