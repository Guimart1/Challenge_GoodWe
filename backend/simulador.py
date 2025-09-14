import random
import requests

API_KEY = "SUA_CHAVE_WEATHER"
CIDADE = "Sao Paulo"

CAPACIDADE_BATERIA = 10000
NIVEL_INICIAL_BATERIA = 5000
CONSUMO_STANDBY = 50
GERACAO_MAXIMA_SOLAR = 500

APARELHOS = {
    "geladeira": 150,
    "tv": 100,
    "computador": 150,
    "microondas": 800
}

def obter_dados_clima():
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CIDADE}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Erro de conexão com a API de clima: {err}")
        return None
    
def calcular_geracao_solar(dados_clima):
    if not dados_clima:
        return 0
    
    condicao_atual = dados_clima['current']['condition']['text'].lower()

    if 'claro' in condicao_atual or 'sol' in condicao_atual:
        fator_clima = 1.0
    elif 'parcialmente nublado' in condicao_atual:
        fator_clima = 0.7
    elif 'nublado' in condicao_atual or 'nevoeiro' in condicao_atual:
        fator_clima = 0.4
    elif 'chuva' in condicao_atual or 'tempestade' in condicao_atual:
        fator_clima = 0.2
    else: fator_clima = 0.6

    geracao_estimada = GERACAO_MAXIMA_SOLAR * fator_clima
    return round(geracao_estimada, 2)

def simular(usar_aparelho="tv", redirecionar_para="bateria"):
    dados_clima = obter_dados_clima()
    if not dados_clima:
        return None
    
    geracao_solar = calcular_geracao_solar(dados_clima)
    nivel_bateria = NIVEL_INICIAL_BATERIA
    consumo_aparelho = APARELHOS.get(usar_aparelho.lower(), 0)
    consumo_total = consumo_aparelho + CONSUMO_STANDBY

    if redirecionar_para == "bateria":
        energia_para_bateria = max(0, geracao_solar - consumo_total)
        novo_nivel = min(nivel_bateria + energia_para_bateria, CAPACIDADE_BATERIA)
    elif redirecionar_para == "casa":
        energia_necessaria = max(0, consumo_total - geracao_solar)
        novo_nivel = nivel_bateria - energia_necessaria if nivel_bateria >= energia_necessaria else nivel_bateria
    else:
        return None
    
    return {
        "cidade": CIDADE,
        "condicao_clima": dados_clima['current']['condition']['text'],
        "temperatura": dados_clima['current']['temp_c'],
        "geracao_solar": geracao_solar,
        "consumo_total": consumo_total,
        "nivel_bateria": novo_nivel,
        "bateria_soc": round(novo_nivel / CAPACIDADE_BATERIA * 100),
        "aparelho_usado": usar_aparelho,
        "redirecionamento": redirecionar_para
    }