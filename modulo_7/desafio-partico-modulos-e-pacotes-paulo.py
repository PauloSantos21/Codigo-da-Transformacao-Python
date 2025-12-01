# atividades_unico.py
# Arquivo único com tratamento de erros e menu

import random
import math

# tentar importar Faker (tratamento se não estiver instalado)
try:
    from faker import Faker
    faker_disponivel = True
except Exception:
    faker_disponivel = False

from datetime import datetime


# --------------------------
# Funções matemáticas
# --------------------------
def soma(a, b):
    return a + b

def subtracao(a, b):
    return a - b

def potencia(base, exp):
    return base ** exp


# --------------------------
# Atividade 1: testar funções matemáticas
# --------------------------
def atividade_1():
    print("\n=== ATIVIDADE 1 — Funções Matemáticas ===")
    print("Soma 5 + 3 =", soma(5, 3))
    print("Subtração 10 - 7 =", subtracao(10, 7))
    print("Potência 2^5 =", potencia(2, 5))


# --------------------------
# Atividade 2: Faker + datetime (com fallback)
# --------------------------
def atividade_2():
    print("\n=== ATIVIDADE 2 — Biblioteca Externa (Faker) ===")
    if faker_disponivel:
        fake = Faker("pt_BR")
        nome = fake.name()
        email = fake.email()
    else:
        # fallback simples caso Faker não esteja instalado
        nome = "Usuario Exemplo"
        email = "usuario@example.com"
        print("Observação: pacote 'faker' não encontrado. Instalando melhora o resultado.")
        print("Para instalar: pip install faker")
    data_atual = datetime.now()

    print("Nome falso:", nome)
    print("Email falso:", email)
    print("Data atual:", data_atual.strftime("%d/%m/%Y %H:%M:%S"))


# --------------------------
# Atividade 3: jogo de adivinhação (com validação)
# --------------------------
def atividade_3():
    print("\n=== ATIVIDADE 3 — Jogo de Adivinhação ===")
    numero_secreto = random.randint(1, 100)
    tentativas = 0
    print("Tente adivinhar o número entre 1 e 100! (digite 'sair' para parar)")

    while True:
        entrada = input("Seu palpite: ").strip()
        if entrada.lower() in ("sair", "exit", "quit"):
            print("Jogo encerrado pelo usuário. O número era:", numero_secreto)
            return

        # validação de número inteiro
        try:
            tentativa = int(entrada)
        except ValueError:
            print("Digite um número inteiro entre 1 e 100 ou 'sair'. Tente novamente.")
            continue

        if tentativa < 1 or tentativa > 100:
            print("Palpite fora do intervalo. Deve ser entre 1 e 100.")
            continue

        tentativas += 1
        diferenca = math.fabs(numero_secreto - tentativa)

        if tentativa == numero_secreto:
            print(f"\n🎉 Parabéns! Você acertou o número {numero_secreto}!")
            print(f"Tentativas: {tentativas}")
            break
        elif tentativa < numero_secreto:
            print("Muito baixo! Tente novamente.")
        else:
            print("Muito alto! Tente novamente.")

        print(f"Diferença da resposta: {diferenca}\n")


# --------------------------
# Desafio extra: explicação (mostrada)
# --------------------------
def desafio_extra():
    print("\n=== DESAFIO EXTRA — Organização de Projeto ===\n")
    exemplo = """Exemplo de organização em pacotes:

meu_projeto/
│
├── utilidades/
│   ├── __init__.py
│   └── calculos.py
│
├── jogos/
│   ├── __init__.py
│   └── adivinhacao.py
│
├── dados/
│   └── gerador.py
│
└── main.py
"""
    print(exemplo)


# --------------------------
# Menu para escolher executar cada atividade
# --------------------------
def menu():
    while True:
        print("\n=== MENU — Escolha uma opção ===")
        print("1 - Testar funções matemáticas")
        print("2 - Gerar dados falsos (Faker) + data")
        print("3 - Jogo de adivinhação")
        print("4 - Mostrar sugestão de organização (desafio extra)")
        print("0 - Sair")
        opc = input("Opção: ").strip()

        if opc == "1":
            atividade_1()
        elif opc == "2":
            atividade_2()
        elif opc == "3":
            # antes de chamar o jogo, avisar que pode bloquear em ambientes sem input
            print("Atenção: o jogo usa input() — rode em terminal/console para jogar.")
            atividade_3()
        elif opc == "4":
            desafio_extra()
        elif opc == "0":
            print("Encerrando. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")


# --------------------------
# Execução principal
# --------------------------
if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário. Saindo...")
