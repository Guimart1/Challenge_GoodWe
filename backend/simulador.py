import random
import requests
from backend.config import *
from backend.operations import *

API_KEY = "6ee1bfa2c7c345ad9fa195342250306"
CIDADE = "Sao Paulo"


def simular(usar_aparelho, redirecionar_para):
    dados_clima = obter_dados_clima()
    if not dados_clima:
        return None

    geracao_solar = calcular_geracao_solar(dados_clima)
    nivel_bateria = NIVEL_INICIAL_BATERIA
    consumo_aparelho = APARELHOS.get(usar_aparelho.lower(), 0)
    consumo_total = consumo_aparelho + CONSUMO_STANDBY

    if redirecionar_para == "bateria":
        energia_para_bateria, novo_nivel = calcular_bateria(geracao_solar, consumo_total, nivel_bateria, CAPACIDADE_BATERIA)
    elif redirecionar_para == "casa":
        energia_necessaria, novo_nivel, _ = calcular_uso_casa(geracao_solar, consumo_total, nivel_bateria)
    else:
        novo_nivel = nivel_bateria

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
