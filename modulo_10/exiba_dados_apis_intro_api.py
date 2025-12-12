import requests # type: ignore
from datetime import datetime
from typing import Optional, Dict, Any


# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

# API Open-Meteo (SEM NECESSIDADE DE CHAVE)
API_URL = "https://geocoding-api.open-meteo.com/v1/search"
API_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


# ============================================================================
# CLASSE PARA ESTRUTURAR DADOS DO TEMPO
# ============================================================================

class DadosTempo:
    """Classe para armazenar dados filtrados de tempo."""
    
    def __init__(self, nome_cidade: str, pais: str, temperatura: float,
                 umidade: int, pressao: float, vento: float, 
                 descricao: str, weather_code: int):
        """Inicializa dados do tempo."""
        self.nome_cidade = nome_cidade
        self.pais = pais
        self.temperatura = temperatura
        self.umidade = umidade
        self.pressao = pressao
        self.vento = vento
        self.descricao = descricao
        self.weather_code = weather_code
        self.data_atualizacao = datetime.now()
    
    def __str__(self):
        """Representação em string."""
        return (f"{self.nome_cidade}, {self.pais} - "
                f"{self.temperatura}°C, {self.descricao}")
    
    def __repr__(self):
        """Representação técnica."""
        return (f"DadosTempo(cidade={self.nome_cidade}, "
                f"temp={self.temperatura}°C, desc={self.descricao})")


# ============================================================================
# FUNÇÕES DE CONSULTA
# ============================================================================

def obter_tempo_cidade(nome_cidade: str, pais_codigo: str = None) -> Optional[DadosTempo]:
    """
    Obtém dados filtrados do tempo de uma cidade.
    
    Args:
        nome_cidade (str): Nome da cidade
        pais_codigo (str): Código do país (opcional)
    
    Returns:
        DadosTempo: Objeto com dados filtrados do tempo
    """
    try:
        # Buscar coordenadas
        parametros_geo = {
            "name": nome_cidade,
            "count": 1,
            "format": "json"
        }
        
        if pais_codigo:
            parametros_geo["country_code"] = pais_codigo
        
        resposta_geo = requests.get(API_URL, params=parametros_geo, timeout=10)
        
        if not resposta_geo.ok or not resposta_geo.json().get("results"):
            print(f"❌ Cidade '{nome_cidade}' não encontrada")
            return None
        
        resultado = resposta_geo.json()["results"][0]
        latitude = resultado["latitude"]
        longitude = resultado["longitude"]
        nome_encontrado = resultado.get("name", nome_cidade)
        pais_encontrado = resultado.get("country", "")
        
        # Buscar dados do tempo
        parametros_tempo = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,pressure_msl",
            "temperature_unit": "celsius",
            "wind_speed_unit": "ms",
            "timezone": "auto"
        }
        
        resposta_tempo = requests.get(API_WEATHER_URL, params=parametros_tempo, timeout=10)
        
        if not resposta_tempo.ok:
            print(f"❌ Erro ao obter tempo")
            return None
        
        # Extrair dados do tempo
        current = resposta_tempo.json().get("current", {})
        temperatura = current.get("temperature_2m", 0)
        umidade = current.get("relative_humidity_2m", 0)
        pressao = current.get("pressure_msl", 0)
        vento = current.get("wind_speed_10m", 0)
        weather_code = current.get("weather_code", 0)
        
        # Mapa de códigos de tempo
        descricoes = {
            0: "Céu limpo",
            1: "Parcialmente nublado",
            2: "Parcialmente nublado",
            3: "Nublado",
            45: "Nevoeiro",
            48: "Nevoeiro",
            51: "Garoa leve",
            53: "Garoa moderada",
            55: "Garoa densa",
            61: "Chuva leve",
            63: "Chuva moderada",
            65: "Chuva pesada",
            71: "Neve leve",
            73: "Neve moderada",
            75: "Neve pesada",
            80: "Pancadas de chuva",
            81: "Pancadas de chuva",
            82: "Pancadas de chuva pesada",
            85: "Pancadas de neve",
            86: "Pancadas de neve",
            95: "Tempestade",
        }
        
        descricao = descricoes.get(weather_code, "Desconhecido")
        
        return DadosTempo(
            nome_encontrado, pais_encontrado, temperatura,
            umidade, pressao, vento, descricao, weather_code
        )
    
    except Exception as erro:
        print(f"❌ Erro: {erro}")
        return None


# ============================================================================
# FUNÇÕES DE EXIBIÇÃO FILTRADA
# ============================================================================

def exibir_resumo_simples(dados: DadosTempo) -> None:
    """
    Exibe apenas temperatura e condições climáticas.
    
    Args:
        dados (DadosTempo): Dados do tempo a exibir
    """
    if not dados:
        return
    
    print(f"\n📍 {dados.nome_cidade}, {dados.pais}")
    print(f"🌡️  Temperatura: {dados.temperatura}°C")
    print(f"☁️  Condições: {dados.descricao}\n")


def exibir_completo(dados: DadosTempo) -> None:
    """
    Exibe informações completas do tempo.
    
    Args:
        dados (DadosTempo): Dados do tempo a exibir
    """
    if not dados:
        return
    
    print("\n" + "=" * 50)
    print(f"  {dados.nome_cidade}, {dados.pais}")
    print("=" * 50)
    print(f"\n🌡️  Temperatura:    {dados.temperatura}°C")
    print(f"💧 Umidade:        {dados.umidade}%")
    print(f"🔽 Pressão:        {dados.pressao} hPa")
    print(f"💨 Vento:          {dados.vento} m/s")
    print(f"☁️  Condições:      {dados.descricao}")
    print(f"⏰ Atualizado:      {dados.data_atualizacao.strftime('%H:%M:%S')}")
    print("=" * 50 + "\n")


def exibir_em_tabela(lista_dados: list) -> None:
    """
    Exibe múltiplas cidades em formato de tabela.
    
    Args:
        lista_dados (list): Lista de DadosTempo
    """
    if not lista_dados:
        print("❌ Nenhum dado para exibir")
        return
    
    print("\n" + "=" * 75)
    print(f"{'Cidade':<20} {'Temp.':<10} {'Umidade':<12} {'Vento':<10} {'Condições':<20}")
    print("=" * 75)
    
    for dados in lista_dados:
        print(f"{dados.nome_cidade:<20} {dados.temperatura:>6.1f}°C   "
              f"{dados.umidade:>9}%   {dados.vento:>8.1f} m/s  "
              f"{dados.descricao:<20}")
    
    print("=" * 75 + "\n")


def exibir_resumo_compacto(dados: DadosTempo) -> None:
    """
    Exibe informações em uma única linha compacta.
    
    Args:
        dados (DadosTempo): Dados do tempo a exibir
    """
    if not dados:
        return
    
    emoji_tempo = {
        "Céu limpo": "☀️",
        "Nublado": "☁️",
        "Chuva": "🌧️",
        "Neve": "❄️",
        "Tempestade": "⛈️",
        "Nevoeiro": "🌫️",
    }
    
    emoji = next(
        (v for k, v in emoji_tempo.items() if k in dados.descricao),
        "🌤️"
    )
    
    print(f"{emoji} {dados.nome_cidade}: {dados.temperatura}°C - {dados.descricao}")


def exibir_apenas_temperatura(dados: DadosTempo) -> None:
    """
    Exibe apenas a temperatura.
    
    Args:
        dados (DadosTempo): Dados do tempo a exibir
    """
    if not dados:
        return
    
    cor = "🔴" if dados.temperatura > 30 else "🟢" if dados.temperatura > 15 else "🔵"
    print(f"{cor} {dados.nome_cidade}: {dados.temperatura}°C")


def exibir_apenas_condicoes(dados: DadosTempo) -> None:
    """
    Exibe apenas as condições climáticas.
    
    Args:
        dados (DadosTempo): Dados do tempo a exibir
    """
    if not dados:
        return
    
    print(f"{dados.nome_cidade}: {dados.descricao}")


# ============================================================================
# FUNÇÕES DE FILTRO E ANÁLISE
# ============================================================================

def filtrar_por_temperatura(lista_dados: list, temp_min: float, temp_max: float) -> list:
    """
    Filtra cidades por faixa de temperatura.
    
    Args:
        lista_dados (list): Lista de DadosTempo
        temp_min (float): Temperatura mínima
        temp_max (float): Temperatura máxima
    
    Returns:
        list: Cidades dentro da faixa de temperatura
    """
    return [d for d in lista_dados if temp_min <= d.temperatura <= temp_max]


def filtrar_por_condicoes(lista_dados: list, condicao: str) -> list:
    """
    Filtra cidades por condições climáticas.
    
    Args:
        lista_dados (list): Lista de DadosTempo
        condicao (str): Palavra-chave da condição
    
    Returns:
        list: Cidades com a condição especificada
    """
    return [d for d in lista_dados if condicao.lower() in d.descricao.lower()]


def obter_cidade_mais_quente(lista_dados: list) -> Optional[DadosTempo]:
    """Retorna a cidade mais quente."""
    return max(lista_dados, key=lambda d: d.temperatura) if lista_dados else None


def obter_cidade_mais_fria(lista_dados: list) -> Optional[DadosTempo]:
    """Retorna a cidade mais fria."""
    return min(lista_dados, key=lambda d: d.temperatura) if lista_dados else None


def obter_temperatura_media(lista_dados: list) -> float:
    """Calcula a temperatura média."""
    if not lista_dados:
        return 0
    return sum(d.temperatura for d in lista_dados) / len(lista_dados)


# ============================================================================
# EXEMPLOS DE USO
# ============================================================================

def exemplo_uso():
    """Demonstra diferentes formas de exibir dados filtrados."""
    
    print("\n" + "=" * 60)
    print(" EXEMPLOS: EXIBINDO DADOS ESPECÍFICOS DA API")
    print("=" * 60)
    
    # Buscar dados de várias cidades
    cidades = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Salvador"]
    lista_dados = []
    
    print("\n🔄 Buscando dados...\n")
    for cidade in cidades:
        dados = obter_tempo_cidade(cidade, "BR")
        if dados:
            lista_dados.append(dados)
    
    # Exemplo 1: Resumo simples (apenas temp e condições)
    print("\n--- Exemplo 1: Resumo Simples ---")
    if lista_dados:
        exibir_resumo_simples(lista_dados[0])
    
    # Exemplo 2: Resumo compacto em uma linha
    print("--- Exemplo 2: Resumo Compacto ---")
    for dados in lista_dados:
        exibir_resumo_compacto(dados)
    
    # Exemplo 3: Apenas temperatura
    print("\n--- Exemplo 3: Apenas Temperatura ---")
    for dados in lista_dados:
        exibir_apenas_temperatura(dados)
    
    # Exemplo 4: Apenas condições
    print("\n--- Exemplo 4: Apenas Condições Climáticas ---")
    for dados in lista_dados:
        exibir_apenas_condicoes(dados)
    
    # Exemplo 5: Tabela comparativa
    print("--- Exemplo 5: Tabela Comparativa ---")
    exibir_em_tabela(lista_dados)
    
    # Exemplo 6: Informações completas
    print("--- Exemplo 6: Informações Completas ---")
    if lista_dados:
        exibir_completo(lista_dados[0])
    
    # Exemplo 7: Análise e filtros
    print("--- Exemplo 7: Análise de Dados ---")
    if lista_dados:
        mais_quente = obter_cidade_mais_quente(lista_dados)
        mais_fria = obter_cidade_mais_fria(lista_dados)
        temp_media = obter_temperatura_media(lista_dados)
        
        print(f"\n📊 Análise de {len(lista_dados)} cidades:")
        print(f"  🔥 Mais quente: {mais_quente.nome_cidade} ({mais_quente.temperatura}°C)")
        print(f"  ❄️  Mais fria: {mais_fria.nome_cidade} ({mais_fria.temperatura}°C)")
        print(f"  📈 Temperatura média: {temp_media:.1f}°C\n")
    
    # Exemplo 8: Filtro por faixa de temperatura
    print("--- Exemplo 8: Filtro por Temperatura (15-25°C) ---")
    filtradas = filtrar_por_temperatura(lista_dados, 15, 25)
    exibir_em_tabela(filtradas)
    
    # Exemplo 9: Filtro por condições
    print("--- Exemplo 9: Cidades com Chuva ---")
    com_chuva = filtrar_por_condicoes(lista_dados, "chuva")
    if com_chuva:
        exibir_em_tabela(com_chuva)
    else:
        print("Nenhuma cidade com chuva no momento.\n")


def menu_interativo():
    """Menu interativo para consultar e exibir dados filtrados."""
    
    print("\n" + "=" * 60)
    print(" CONSULTOR DE TEMPO - EXIBIÇÃO FILTRADA")
    print("=" * 60)
    
    while True:
        print("\n1. Buscar cidade (resumo simples)")
        print("2. Buscar cidade (informações completas)")
        print("3. Buscar apenas temperatura")
        print("4. Buscar apenas condições climáticas")
        print("5. Comparar múltiplas cidades")
        print("6. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            cidade = input("Digite o nome da cidade: ").strip()
            dados = obter_tempo_cidade(cidade, "BR")
            exibir_resumo_simples(dados)
        
        elif opcao == "2":
            cidade = input("Digite o nome da cidade: ").strip()
            dados = obter_tempo_cidade(cidade, "BR")
            exibir_completo(dados)
        
        elif opcao == "3":
            cidade = input("Digite o nome da cidade: ").strip()
            dados = obter_tempo_cidade(cidade, "BR")
            exibir_apenas_temperatura(dados)
            print()
        
        elif opcao == "4":
            cidade = input("Digite o nome da cidade: ").strip()
            dados = obter_tempo_cidade(cidade, "BR")
            exibir_apenas_condicoes(dados)
            print()
        
        elif opcao == "5":
            num_cidades = int(input("Quantas cidades? "))
            lista = []
            
            for i in range(num_cidades):
                cidade = input(f"Cidade {i+1}: ").strip()
                dados = obter_tempo_cidade(cidade, "BR")
                if dados:
                    lista.append(dados)
            
            exibir_em_tabela(lista)
        
        elif opcao == "6":
            print("Encerrando...")
            break
        
        else:
            print("❌ Opção inválida!")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    exemplo_uso()
    
    # Descomente para usar menu interativo
    # resposta = input("Deseja usar o menu interativo? (s/n): ").strip().lower()
    # if resposta == "s":
    #     menu_interativo()