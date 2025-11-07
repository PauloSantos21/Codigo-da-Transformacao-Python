'''
COMPARANDO NÚMEROS COM IF-ELIF-ELSE
Este programa decide qual de dois números é o maior.
Peça ao usuário para digitar 2 números inteiros e mostre:
- Qual número é o maior
- Ou se são iguais  

'''

print("\n--- Comparador de Números ---")

try:
    numero1 = int(input("Digite um número inteiro (EX: 1): "))
    numero2 = int(input("Digite outro número: "))
except ValueError:
    print("Digite um número válido!")
    exit()


print("\n--- Resultado da Comparação ---")

if numero1 > numero2:
    print(f"O número {numero1} é o maior")

elif numero2 > numero1:
    print(f"O numero {numero2} é o maior")

else:
    print("Ambos são iguais")
