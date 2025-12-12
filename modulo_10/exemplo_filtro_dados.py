"""
EXEMPLO: Exibindo Dados Filtrados da API

Demonstra diferentes formas de exibir e filtrar dados específicos
como temperatura e condições climáticas.
"""

# ============================================================================
# DADOS SIMULADOS (para teste rápido sem chamar API)
# ============================================================================

class DadosTempo:
    """Classe para armazenar dados do tempo."""
    
    def __init__(self, cidade, pais, temperatura, umidade, pressao, vento, condicao):
        self.cidade = cidade
        self.pais = pais
        self.temperatura = temperatura
        self.umidade = umidade
        self.pressao = pressao
        self.vento = vento
        self.condicao = condicao
    
    def __str__(self):
        return f"{self.cidade}: {self.temperatura}°C - {self.condicao}"


# Dados de exemplo
DADOS = [
    DadosTempo("São Paulo", "BR", 22, 65, 1004, 3.2, "Parcialmente nublado"),
    DadosTempo("Rio de Janeiro", "BR", 26, 72, 1008, 4.1, "Céu limpo"),
    DadosTempo("Salvador", "BR", 28, 78, 1010, 5.5, "Céu limpo"),
    DadosTempo("Belo Horizonte", "BR", 20, 68, 1006, 2.8, "Nublado"),
    DadosTempo("Curitiba", "BR", 18, 62, 1012, 2.1, "Chuva leve"),
    DadosTempo("Porto Alegre", "BR", 16, 59, 1014, 3.5, "Nublado"),
]


# ============================================================================
# FUNÇÕES DE EXIBIÇÃO FILTRADA
# ============================================================================

def exibir_resumo_simples(dados):
    """Exibe apenas temperatura e condições."""
    print(f"\n📍 {dados.cidade}, {dados.pais}")
    print(f"🌡️  {dados.temperatura}°C - {dados.condicao}\n")


def exibir_apenas_temperatura(dados):
    """Exibe apenas a temperatura."""
    cor = "🔴" if dados.temperatura > 25 else "🟢" if dados.temperatura > 18 else "🔵"
    print(f"{cor} {dados.cidade}: {dados.temperatura}°C")


def exibir_apenas_condicoes(dados):
    """Exibe apenas as condições climáticas."""
    print(f"{dados.cidade}: {dados.condicao}")


def exibir_em_tabela(lista_dados):
    """Exibe múltiplas cidades em tabela."""
    print("\n" + "=" * 70)
    print(f"{'Cidade':<20} {'Temp.':<10} {'Umidade':<12} {'Vento':<10} {'Condição':<15}")
    print("=" * 70)
    
    for d in lista_dados:
        print(f"{d.cidade:<20} {d.temperatura:>6}°C    "
              f"{d.umidade:>9}%   {d.vento:>8.1f} m/s  {d.condicao:<15}")
    
    print("=" * 70 + "\n")


def exibir_completo(dados):
    """Exibe informações completas."""
    print("\n" + "=" * 50)
    print(f"  {dados.cidade}, {dados.pais}")
    print("=" * 50)
    print(f"🌡️  Temperatura:    {dados.temperatura}°C")
    print(f"💧 Umidade:        {dados.umidade}%")
    print(f"🔽 Pressão:        {dados.pressao} hPa")
    print(f"💨 Vento:          {dados.vento} m/s")
    print(f"☁️  Condições:      {dados.condicao}")
    print("=" * 50 + "\n")


# ============================================================================
# FUNÇÕES DE FILTRO
# ============================================================================

def filtrar_por_temperatura(lista, temp_min, temp_max):
    """Filtra por faixa de temperatura."""
    return [d for d in lista if temp_min <= d.temperatura <= temp_max]


def filtrar_por_condicoes(lista, condicao_chave):
    """Filtra por condições climáticas."""
    return [d for d in lista if condicao_chave.lower() in d.condicao.lower()]


def obter_cidade_mais_quente(lista):
    """Retorna a cidade mais quente."""
    return max(lista, key=lambda d: d.temperatura)


def obter_cidade_mais_fria(lista):
    """Retorna a cidade mais fria."""
    return min(lista, key=lambda d: d.temperatura)


def obter_temperatura_media(lista):
    """Calcula temperatura média."""
    return sum(d.temperatura for d in lista) / len(lista)


# ============================================================================
# EXEMPLOS
# ============================================================================

def main():
    print("\n" + "=" * 60)
    print(" EXEMPLOS: EXIBINDO DADOS ESPECÍFICOS FILTRADOS")
    print("=" * 60)
    
    # Exemplo 1: Resumo simples
    print("\n--- Exemplo 1: Resumo Simples (Temp + Condições) ---")
    exibir_resumo_simples(DADOS[0])
    
    # Exemplo 2: Apenas temperatura
    print("--- Exemplo 2: Apenas Temperatura ---")
    for dados in DADOS:
        exibir_apenas_temperatura(dados)
    
    # Exemplo 3: Apenas condições
    print("\n--- Exemplo 3: Apenas Condições Climáticas ---")
    for dados in DADOS:
        exibir_apenas_condicoes(dados)
    
    # Exemplo 4: Tabela comparativa
    print("\n--- Exemplo 4: Tabela Comparativa ---")
    exibir_em_tabela(DADOS)
    
    # Exemplo 5: Informações completas
    print("--- Exemplo 5: Informações Completas ---")
    exibir_completo(DADOS[0])
    
    # Exemplo 6: Análise de dados
    print("--- Exemplo 6: Análise de Dados ---")
    mais_quente = obter_cidade_mais_quente(DADOS)
    mais_fria = obter_cidade_mais_fria(DADOS)
    media = obter_temperatura_media(DADOS)
    
    print(f"\n📊 Análise de {len(DADOS)} cidades:")
    print(f"  🔥 Mais quente: {mais_quente.cidade} ({mais_quente.temperatura}°C)")
    print(f"  ❄️  Mais fria: {mais_fria.cidade} ({mais_fria.temperatura}°C)")
    print(f"  📈 Temperatura média: {media:.1f}°C\n")
    
    # Exemplo 7: Filtro por faixa de temperatura
    print("--- Exemplo 7: Filtrar Cidades (18-23°C) ---")
    filtradas = filtrar_por_temperatura(DADOS, 18, 23)
    exibir_em_tabela(filtradas)
    
    # Exemplo 8: Filtro por condições
    print("--- Exemplo 8: Cidades com Céu Limpo ---")
    com_ceu_limpo = filtrar_por_condicoes(DADOS, "céu limpo")
    exibir_em_tabela(com_ceu_limpo)
    
    # Exemplo 9: Filtro por chuva
    print("--- Exemplo 9: Cidades com Chuva ---")
    com_chuva = filtrar_por_condicoes(DADOS, "chuva")
    exibir_em_tabela(com_chuva)
    
    # Exemplo 10: Cidades quentes
    print("--- Exemplo 10: Cidades Quentes (≥ 25°C) ---")
    quentes = filtrar_por_temperatura(DADOS, 25, 50)
    exibir_em_tabela(quentes)
    
    # Exemplo 11: Exibição compacta
    print("--- Exemplo 11: Exibição Compacta ---")
    for dados in DADOS:
        emoji_temp = "🔴" if dados.temperatura > 25 else "🟢" if dados.temperatura > 18 else "🔵"
        print(f"{emoji_temp} {dados.cidade:<20} {dados.temperatura}°C  {dados.condicao}")


if __name__ == "__main__":
    main()