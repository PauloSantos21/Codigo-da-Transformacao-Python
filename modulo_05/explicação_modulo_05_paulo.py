import json


import json
import os

def calcula_media(notas):
    """Calcula a média de uma lista de notas."""
    return sum(notas) / len(notas)

def verificar_aprovacao(media):
    """Verifica se o aluno foi aprovado (média >= 7)."""
    if media >= 7:
        return "Aprovado"
    else:
        return "Reprovado"


db_file = 'alunos_db.json'
if os.path.exists(db_file):
    with open(db_file, 'r') as f:
        alunos_db = json.load(f)
else:
    alunos_db = []

nome_aluno = input("Insira o nome do aluno: ")
notas_input = input("Insira as notas do aluno separadas por vírgula: ")
notas_aluno = [float(nota) for nota in notas_input.split(',')]

media_final = calcula_media(notas_aluno)
status_aluno = verificar_aprovacao(media_final)

aluno = {
    'nome': nome_aluno,
    'notas': notas_aluno,
    'media': media_final,
    'status': status_aluno
}
alunos_db.append(aluno)


with open(db_file, 'w') as f:
    json.dump(alunos_db, f, indent=4)

print(f"Notas: {notas_aluno}")
print(f"Média: {media_final:.2f}")
print(f"Status: {status_aluno}")

print("\nBanco de Dados de Alunos:")
for aluno in alunos_db:
    print(f"Nome: {aluno['nome']}, Notas: {aluno['notas']}, Média: {aluno['media']:.2f}, Status: {aluno['status']}")