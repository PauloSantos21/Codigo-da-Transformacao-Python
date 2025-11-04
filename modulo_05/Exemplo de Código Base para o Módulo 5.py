# Exemplo de Código Base para o Módulo 5

def calcula_media(notas):
    """Calcula a média de uma lista de notas."""
    # sum(notas) soma todos os itens da lista
    # len(notas) conta quantos itens há na lista
    return sum(notas) / len(notas) # 

def verificar_aprovacao(media):
    """Verifica se o aluno foi aprovado (média >= 7)."""
    if media >= 7:
        return "Aprovado" # 
    else:
        return "Reprovado" # 

# Notas do aluno
notas_aluno = [8.0, 7.5, 6.0, 9.5]

# Chamando as funções
media_final = calcula_media(notas_aluno)
status_aluno = verificar_aprovacao(media_final)

# Exibindo o resultado
print(f"Notas: {notas_aluno}")
print(f"Média: {media_final:.2f}")
print(f"Status: {status_aluno}")