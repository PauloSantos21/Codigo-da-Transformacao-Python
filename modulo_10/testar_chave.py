import requests # type: ignore

API_KEY = "70bed771282ecdac0890a5c60b0ee8cf"
API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Teste simples
parametros = {
    "q": "São Paulo,BR",
    "appid": API_KEY,
    "units": "metric",
    "lang": "pt"
}

print("Testando conexão com API...")
print(f"API Key: {API_KEY[:10]}...")
print(f"URL: {API_URL}\n")

resposta = requests.get(API_URL, params=parametros, timeout=5)

print(f"Status Code: {resposta.status_code}")
print(f"Response: {resposta.text[:200]}\n")

if resposta.status_code == 200:
    print("✓ Sucesso!")
    dados = resposta.json()
    print(f"Cidade: {dados['name']}")
    print(f"Temperatura: {dados['main']['temp']}°C")
elif resposta.status_code == 401:
    print("❌ Erro 401: API key inválida ou não autorizada")
    print("Possíveis causas:")
    print("- Chave expirou")
    print("- Chave não está ativa")
    print("- Chave tem restrições de uso")
elif resposta.status_code == 404:
    print("❌ Erro 404: Cidade não encontrada")
else:
    print(f"❌ Erro {resposta.status_code}")