import requests
from config import API_KEY, CIDADE, GERACAO_MAXIMA_SOLAR

def obter_dados_clima():
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CIDADE}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def calcular_geracao_solar(dados_clima):
    if not dados_clima:
        return 0
    condicao = dados_clima['current']['condition']['text'].lower()
    if 'claro' in condicao or 'sol' in condicao:
        fator = 1.0
    elif 'parcialmente nublado' in condicao:
        fator = 0.7
    elif 'nublado' in condicao or 'nevoeiro' in condicao:
        fator = 0.4
    elif 'chuva' in condicao or 'tempestade' in condicao:
        fator = 0.2
    else:
        fator = 0.6
    return round(GERACAO_MAXIMA_SOLAR * fator, 2)
