import os
import requests
import random
from datetime import datetime

from flask.cli import load_dotenv

from backend.config import CIDADE, GERACAO_MAXIMA_SOLAR, APARELHOS, CONSUMO_STANDBY, CAPACIDADE_BATERIA
from backend.conexao_sems import crosslogin, get_inverter_list_demo, get_full_battery_status
import os



def get_sems_token():
    acc = os.getenv("SEMS_ACCOUNT", "demo@goodwe.com")
    pwd = os.getenv("SEMS_PASSWORD", "GoodweSems123!@#")
    token = crosslogin(acc, pwd, region="us")
    return token


def get_battery_status(token):
    inverters = get_inverter_list_demo(token, region="eu")
    if not inverters.get("data"):
        return None
    inverter_id = inverters["data"][0]["id"]
    status = get_full_battery_status(token, inverter_id, region="eu")
    return status


# --- FUNÇÕES DE SIMULAÇÃO E CÁLCULO (JÁ EXISTENTES) ---

def obter_dados_clima():
    """Busca dados de clima e temperatura da API do WeatherAPI."""
    url = f"http://api.weatherapi.com/v1/current.json?key={os.getenv("WEATHER_API_KEY")}&q={CIDADE}&lang=pt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        # A função já retorna None se uma exceção ocorrer,
        # então não há necessidade de um 'pass' aqui.
        return None

def calcular_geracao_solar(dados_clima):
    if not dados_clima:
        return 0

    hora_atual = datetime.now().hour
    if hora_atual < 6 or hora_atual > 18:
        return 0

    condicao = dados_clima['current']['condition']['text'].lower()
    if 'sol' in condicao:
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


def obter_nivel_bateria_real():
    """Obtém o nível de carga real da bateria através da API SEMS."""
    token = get_sems_token()
    status = get_battery_status(token)

    if status is None:
        # Retorna um valor padrão ou levanta uma exceção para o chamador tratar.
        # Retornar 0 é uma opção segura para evitar o erro.
        return 0

    return status["soc"]


def simular(comodo, usar_aparelho, redirecionar_para, nivel_bateria_real):
    """Simula o consumo de energia da residência."""
    dados_clima = obter_dados_clima()
    if not dados_clima:
        return None
    geracao_solar = calcular_geracao_solar(dados_clima)
    consumo_aparelho = APARELHOS.get(comodo, {}).get(usar_aparelho.lower(), 0)
    consumo_total = consumo_aparelho + CONSUMO_STANDBY

    bateria_soc = round(nivel_bateria_real / CAPACIDADE_BATERIA * 100)

    return {
        "cidade": CIDADE,
        "condicao_clima": dados_clima['current']['condition']['text'],
        "temperatura": dados_clima['current']['temp_c'],
        "geracao_solar": geracao_solar,
        "consumo_total": consumo_total,
        "nivel_bateria": nivel_bateria_real,
        "bateria_soc": bateria_soc,
        "aparelho_usado": usar_aparelho,
        "redirecionamento": redirecionar_para
    }