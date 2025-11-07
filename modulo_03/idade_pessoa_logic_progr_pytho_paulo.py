"""
Idade pessoa
pergunta pra pessoa nome e idade
guarda em variaveis
verifíca a faixa etária da pessoa


"""


nome = str(input("Qual seu nome: "))
idade = int(input("Qual sua idade: "))


if idade <= 10: 
    print(f"Olá {nome}, você é uma criança")

elif idade <= 17:
    print(f"Olá {nome}, você é um adolescente")

elif idade <= 59:
    print(f"Olá {nome}, você é um adulto")

else:
    print(f"Olá {nome}, você é um idoso")