import requests # type: ignore
import json
from datetime import datetime
from typing import Optional, Dict, Any


# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

# API Open-Meteo (SEM NECESSIDADE DE CHAVE)
# Documentação: https://open-meteo.com/en/docs
API_URL = "https://geocoding-api.open-meteo.com/v1/search"
API_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


# ============================================================================
# EXCEÇÕES PERSONALIZADAS
# ============================================================================

class APIError(Exception):
    """Exceção para erros gerais de API."""
    pass


class CidadeNaoEncontradaError(APIError):
    """Exceção quando cidade não é encontrada."""
    pass


class APIKeyInvalidaError(APIError):
    """Exceção quando API key é inválida."""
    pass


class ConexaoError(APIError):
    """Exceção para problemas de conexão."""
    pass


# ============================================================================
# FUNÇÕES DE CONSUMO DE API
# ============================================================================

def obter_tempo_cidade(nome_cidade: str, pais_codigo: str = None, 
                      idioma: str = "pt") -> Optional[Dict[str, Any]]:
    """
    Obtém informações do tempo atual para uma cidade.
    
    Args:
        nome_cidade (str): Nome da cidade
        pais_codigo (str): Código do país (opcional, ex: "BR")
        idioma (str): Idioma da resposta
    
    Returns:
        dict: Dados do tempo ou None se erro
    
    Raises:
        CidadeNaoEncontradaError: Se cidade não encontrada
        ConexaoError: Se erro de conexão
    """
    try:
        # Buscar coordenadas da cidade
        print(f"🌐 Buscando coordenadas de {nome_cidade}...")
        
        parametros_geo = {
            "name": nome_cidade,
            "count": 1,
            "language": idioma,
            "format": "json"
        }
        
        if pais_codigo:
            parametros_geo["country_code"] = pais_codigo
        
        resposta_geo = requests.get(API_URL, params=parametros_geo, timeout=5)
        
        if resposta_geo.status_code != 200:
            raise APIError(f"Erro ao buscar cidade: {resposta_geo.status_code}")
        
        dados_geo = resposta_geo.json()
        
        if not dados_geo.get("results"):
            raise CidadeNaoEncontradaError(f"Cidade '{nome_cidade}' não encontrada")
        
        # Pegar primeira resultado
        resultado = dados_geo["results"][0]
        latitude = resultado["latitude"]
        longitude = resultado["longitude"]
        nome_encontrado = resultado.get("name", nome_cidade)
        pais_encontrado = resultado.get("country", "")
        
        # Buscar dados do tempo
        print(f"🌐 Conectando à API Open-Meteo...")
        
        parametros_tempo = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,pressure_msl",
            "temperature_unit": "celsius",
            "wind_speed_unit": "ms",
            "timezone": "auto"
        }
        
        resposta_tempo = requests.get(API_WEATHER_URL, params=parametros_tempo, timeout=5)
        
        if resposta_tempo.status_code != 200:
            raise APIError(f"Erro ao obter tempo: {resposta_tempo.status_code}")
        
        dados_tempo = resposta_tempo.json()
        
        # Estruturar resposta similar ao OpenWeatherMap
        return {
            "name": nome_encontrado,
            "country": pais_encontrado,
            "latitude": latitude,
            "longitude": longitude,
            "current": dados_tempo.get("current", {}),
            "timezone": dados_tempo.get("timezone", "")
        }
    
    except CidadeNaoEncontradaError:
        raise
    except requests.exceptions.ConnectionError:
        raise ConexaoError("Erro de conexão. Verifique sua internet.")
    except requests.exceptions.Timeout:
        raise ConexaoError("Tempo de conexão expirou.")
    except requests.exceptions.RequestException as e:
        raise ConexaoError(f"Erro na requisição: {e}")


def obter_previsao_cidade(nome_cidade: str, pais_codigo: str = None,
                         idioma: str = "pt") -> Optional[Dict[str, Any]]:
    """
    Obtém previsão do tempo para os próximos dias.
    
    Args:
        nome_cidade (str): Nome da cidade
        pais_codigo (str): Código do país (opcional)
        idioma (str): Idioma da resposta
    
    Returns:
        dict: Dados de previsão ou None se erro
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
        
        resposta_geo = requests.get(API_URL, params=parametros_geo, timeout=5)
        
        if not resposta_geo.ok or not resposta_geo.json().get("results"):
            raise CidadeNaoEncontradaError(f"Cidade '{nome_cidade}' não encontrada")
        
        resultado = resposta_geo.json()["results"][0]
        latitude = resultado["latitude"]
        longitude = resultado["longitude"]
        
        # Buscar previsão
        parametros_tempo = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m,relative_humidity_2m,weather_code,precipitation",
            "temperature_unit": "celsius",
            "timezone": "auto"
        }
        
        resposta_tempo = requests.get(API_WEATHER_URL, params=parametros_tempo, timeout=5)
        
        if not resposta_tempo.ok:
            raise APIError(f"Erro: {resposta_tempo.status_code}")
        
        return resposta_tempo.json()
    
    except requests.exceptions.RequestException as e:
        raise ConexaoError(f"Erro de conexão: {e}")


def obter_tempo_coordenadas(latitude: float, longitude: float,
                           idioma: str = "pt") -> Optional[Dict[str, Any]]:
    """
    Obtém tempo usando coordenadas geográficas.
    
    Args:
        latitude (float): Latitude
        longitude (float): Longitude
        idioma (str): Idioma da resposta
    
    Returns:
        dict: Dados do tempo
    """
    try:
        parametros = {
            "lat": latitude,
            "lon": longitude,
            "appid": API_KEY,  # pyright: ignore[reportUndefinedVariable]
            "units": "metric",
            "lang": idioma
        }
        
        resposta = requests.get(API_URL, params=parametros, timeout=5)
        
        if resposta.status_code != 200:
            raise APIError(f"Erro: {resposta.status_code}")
        
        return resposta.json()
    
    except requests.exceptions.RequestException as e:
        raise ConexaoError(f"Erro: {e}")


# ============================================================================
# FUNÇÕES DE FORMATAÇÃO E EXIBIÇÃO
# ============================================================================

def exibir_tempo(dados_tempo: Dict[str, Any]) -> None:
    """
    Exibe informações do tempo de forma formatada.
    
    Args:
        dados_tempo (dict): Dados retornados pela API
    """
    try:
        # Extrair informações
        cidade = dados_tempo.get("name", "Desconhecido")
        pais = dados_tempo.get("country", "")
        
        current = dados_tempo.get("current", {})
        temperatura = current.get("temperature_2m", "N/A")
        umidade = current.get("relative_humidity_2m", "N/A")
        pressao = current.get("pressure_msl", "N/A")
        velocidade_vento = current.get("wind_speed_10m", "N/A")
        weather_code = current.get("weather_code", 0)
        
        # Descrição do código de tempo
        descricoes_tempo = {
            0: "Céu limpo",
            1: "Céu parcialmente nublado",
            2: "Céu parcialmente nublado",
            3: "Céu nublado",
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
            80: "Pancadas de chuva leve",
            81: "Pancadas de chuva moderada",
            82: "Pancadas de chuva pesada",
            85: "Pancadas de neve leve",
            86: "Pancadas de neve pesada",
            95: "Tempestade",
        }
        
        descricao = descricoes_tempo.get(weather_code, "Desconhecido")
        
        # Emoji apropriado
        descricoes_emoji = {
            "céu limpo": "☀️",
            "nublado": "☁️",
            "chuva": "🌧️",
            "neve": "❄️",
            "tempestade": "⛈️",
            "nevoeiro": "🌫️",
            "garoa": "🌦️"
        }
        
        emoji = next(
            (v for k, v in descricoes_emoji.items() if k in descricao.lower()),
            "🌤️"
        )
        
        # Imprimir informações
        print("\n" + "=" * 60)
        print(f" 🌍 CLIMA - {cidade}, {pais}")
        print("=" * 60)
        
        print(f"\n{emoji} Condições: {descricao}")
        print(f"\n🌡️  Temperatura: {temperatura}°C")
        print(f"💧 Umidade: {umidade}%")
        print(f"🔽 Pressão: {pressao} hPa")
        print(f"💨 Vento: {velocidade_vento} m/s")
        
        # Hora da atualização
        print(f"\n⏰ Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        print("=" * 60 + "\n")
    
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")


def exibir_previsao(dados_previsao: Dict[str, Any], dias: int = 1) -> None:
    """
    Exibe previsão do tempo.
    
    Args:
        dados_previsao (dict): Dados de previsão
        dias (int): Número de dias a mostrar
    """
    try:
        cidade = dados_previsao.get("city", {}).get("name", "Desconhecido")
        pais = dados_previsao.get("city", {}).get("country", "")
        
        print("\n" + "=" * 60)
        print(f" 📅 PREVISÃO DO TEMPO - {cidade}, {pais}")
        print("=" * 60)
        
        lista_previsoes = dados_previsao.get("list", [])
        previsoes_dia = []
        data_atual = None
        
        for previsao in lista_previsoes:
            timestamp = previsao.get("dt", 0)
            data = datetime.fromtimestamp(timestamp)
            
            if data_atual is None or data.date() != data_atual.date():
                if data_atual is not None and len(previsoes_dia) > 0:
                    _exibir_dia_previsao(data_atual, previsoes_dia)
                    if datetime.now().date() != data.date() and len(previsoes_dia) >= dias:
                        break
                
                data_atual = data
                previsoes_dia = [previsao]
            else:
                previsoes_dia.append(previsao)
        
        # Exibir último dia
        if previsoes_dia and (datetime.now().date() != data_atual.date() or dias == 1):
            _exibir_dia_previsao(data_atual, previsoes_dia)
        
        print("=" * 60 + "\n")
    
    except Exception as e:
        print(f"❌ Erro ao exibir previsão: {e}")


def _exibir_dia_previsao(data: datetime, previsoes: list) -> None:
    """Função auxiliar para exibir previsão de um dia."""
    print(f"\n📅 {data.strftime('%d/%m/%Y')}")
    
    for previsao in previsoes[:4]:  # Mostrar 4 previsões por dia
        timestamp = previsao.get("dt", 0)
        hora = datetime.fromtimestamp(timestamp).strftime("%H:%M")
        temp = previsao.get("main", {}).get("temp", "N/A")
        descricao = previsao.get("weather", [{}])[0].get("description", "N/A")
        chuva = previsao.get("pop", 0) * 100  # Probabilidade de chuva
        
        print(f"  {hora} - {temp}°C - {descricao.capitalize()} "
              f"(Chuva: {chuva:.0f}%)")


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

def exemplo_uso():
    """Demonstra o uso do sistema de consulta de tempo."""
    
    print("\n" + "=" * 60)
    print(" EXEMPLOS: CONSUMINDO API OPEN-METEO (SEM CHAVE!)")
    print("=" * 60 + "\n")
    
    # Exemplo 1: Tempo atual
    print("--- Exemplo 1: Tempo Atual em São Paulo ---\n")
    try:
        dados = obter_tempo_cidade("São Paulo", "BR")
        if dados:
            exibir_tempo(dados)
    except CidadeNaoEncontradaError as e:
        print(f"❌ Erro: {e}\n")
    except ConexaoError as e:
        print(f"❌ Erro: {e}\n")
    
    # Exemplo 2: Tempo em outra cidade
    print("--- Exemplo 2: Tempo em Nova York ---\n")
    try:
        dados = obter_tempo_cidade("New York", "US")
        if dados:
            exibir_tempo(dados)
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Exemplo 3: Previsão do tempo
    print("--- Exemplo 3: Previsão de São Paulo ---\n")
    try:
        dados = obter_previsao_cidade("São Paulo", "BR")
        if dados:
            exibir_previsao(dados, dias=2)
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Exemplo 4: Outra cidade
    print("--- Exemplo 4: Tempo no Rio de Janeiro ---\n")
    try:
        dados = obter_tempo_cidade("Rio de Janeiro", "BR")
        if dados:
            exibir_tempo(dados)
    except Exception as e:
        print(f"❌ Erro: {e}\n")


def menu_interativo():
    """Menu interativo para consultar o tempo."""
    
    while True:
        print("\n" + "=" * 60)
        print(" CONSULTOR DE TEMPO (API OPEN-METEO)")
        print("=" * 60)
        print("\n1. Obter tempo atual de uma cidade")
        print("2. Obter previsão de uma cidade")
        print("3. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            cidade = input("Digite o nome da cidade: ").strip()
            pais = input("Código do país (opcional, ex: BR): ").strip() or None
            
            try:
                dados = obter_tempo_cidade(cidade, pais)
                if dados:
                    exibir_tempo(dados)
            except CidadeNaoEncontradaError as e:
                print(f"\n❌ Erro: {e}\n")
            except ConexaoError as e:
                print(f"\n❌ Erro: {e}\n")
        
        elif opcao == "2":
            cidade = input("Digite o nome da cidade: ").strip()
            pais = input("Código do país (opcional): ").strip() or None
            
            try:
                dados = obter_previsao_cidade(cidade, pais)
                if dados:
                    exibir_previsao(dados, dias=3)
            except Exception as e:
                print(f"\n❌ Erro: {e}\n")
        
        elif opcao == "3":
            print("Encerrando...")
            break
        
        else:
            print("❌ Opção inválida!")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Executar exemplos
    exemplo_uso()
    
    # Menu interativo (descomente para usar)
    # resposta = input("Deseja usar o menu interativo? (s/n): ").strip().lower()
    # if resposta == "s":
    #     menu_interativo()