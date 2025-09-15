import requests
from backend.config import API_KEY, CIDADE, GERACAO_MAXIMA_SOLAR
import streamlit as st
from datetime import datetime


def obter_dados_clima():
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CIDADE}&lang=pt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
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


def calcular_consumo(aparelho, aparelhos, standby):
    return aparelhos.get(aparelho, 0) + standby

def calcular_bateria(geracao, consumo, nivel_bateria, capacidade):
    energia_para_bateria = max(0, geracao - consumo)
    novo_nivel = min(nivel_bateria + energia_para_bateria, capacidade)
    return energia_para_bateria, novo_nivel

def calcular_uso_casa(geracao, consumo, nivel_bateria):
    energia_necessaria = max(0, consumo - geracao)
    if nivel_bateria >= energia_necessaria:
        novo_nivel = nivel_bateria - energia_necessaria
        return energia_necessaria, novo_nivel, True
    else:
        return energia_necessaria, nivel_bateria, False















