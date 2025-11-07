'''
OPERADORES ARITMÉTICOS
Este programa demonstra as 5 operações básicas com 2 números.
Peça ao usuario para digitar 2 números inteiros e mostre:
- A soma
- A diferença (subtração)
- A multiplicação
- A divisão
- O módulo (resto da divisão)

'''


try:
    numero1 = float(input("Digite um numero: "))
    numero2 = float(input("Digite outro numero: "))
except ValueError:
    print("\nVoce digitou um numero errado! tente novamente")
    exit()

print("\n--- Resultados das Operações ---")

soma = numero1 + numero2
print(f"A soma de '{numero1}' e '{numero2}' é = {soma}\n\n")

subtracao = numero1 - numero2
print(f"A subtração entre '{numero1}' e '{numero2}' é = {subtracao}\n\n")

divisao = numero1 / numero2
print(f"A divisão entre '{numero1}' e '{numero2}' é = {divisao}\n\n")

multiplicacao = numero1 * numero2
print(f"A multiplicação entre '{numero1}' e '{numero2}' é = {multiplicacao}\n\n")

resto_divisao = numero1 % numero2
print(f"O resto da divisão entre '{numero1}' e '{numero2}' é = {resto_divisao}\n\n")