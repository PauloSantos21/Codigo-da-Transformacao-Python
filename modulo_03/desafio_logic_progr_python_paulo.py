# Funções de Operações
def soma(a, b):
    return a + b

def subtracao(a, b):
    return a - b

def multiplicacao(a, b):
    return a * b

def divisao(a, b):
    return a / b

def menu_calculadora():
    executando = True

    while executando:
        
        print("\n--- Menu Interativo ---")
        print("1. Soma")
        print("2. Subtração")
        print("3. Multiplicação") 
        print("4. Divisão")       
        print("5. Sair")          
        print("-----------------------")

       
        escolha = input("Digite o número da opção desejada: ")

        
        if escolha == '1': 
            try:
                num1 = float(input("Digite o primeiro número: "))
                num2 = float(input("Digite o segundo número: "))
                resultado = soma(num1, num2)
                print(f"\n✅ Resultado da Soma: {resultado}")
            except ValueError:
                print("\n❌ Entrada inválida. Por favor, digite números válidos.")

        elif escolha == '2': 
            try:
                num1 = float(input("Digite o primeiro número (Minuendo): "))
                num2 = float(input("Digite o segundo número (Subtraendo): "))
                resultado = subtracao(num1, num2)
                print(f"\n✅ Resultado da Subtração: {resultado}")
            except ValueError:
                print("\n❌ Entrada inválida. Por favor, digite números válidos.")

        elif escolha == '3': 
            try:
                num1 = float(input("Digite o primeiro número: "))
                num2 = float(input("Digite o segundo número: "))
                resultado = multiplicacao(num1, num2)
                print(f"\n✅ Resultado da Multiplicação: {resultado}")
            except ValueError:
                print("\n❌ Entrada inválida. Por favor, digite números válidos.")

        elif escolha == '4': 
            try:
                num1 = float(input("Digite o dividendo: "))
                num2 = float(input("Digite o divisor: "))
                
                resultado = divisao(num1, num2)
                
                print(f"\n✅ Resultado da Divisão: {resultado}")

            except ZeroDivisionError:
                print("\n❌ Dividir por 0 é complicado né burro")

            except ValueError:
                print("\n❌ Entrada inválida. Por favor, digite números válidos.")

        elif escolha == '5': 
            executando = False
            print("\n👋 Programa encerrado. Obrigado por utilizar!")

        else:
            print("\n⚠️ Opção inválida. Por favor, escolha um número de 1 a 5.")


menu_calculadora()