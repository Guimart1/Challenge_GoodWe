import random
import requests
from backend.config import *
from backend.operations import *
from dotenv import load_dotenv
load_dotenv()

# Edite .env.example com sua chave API
weather_key = os.getenv("WEATHER_API_KEY")
CIDADE = "Sao Paulo"


def simular(comodo, usar_aparelho, redirecionar_para, nivel_bateria_real):
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

