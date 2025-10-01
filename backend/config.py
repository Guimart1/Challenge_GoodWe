import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")
CIDADE = 'São Paulo'

CAPACIDADE_BATERIA = 10000
NIVEL_INICIAL_BATERIA = 1000
CONSUMO_STANDBY = 50
GERACAO_MAXIMA_SOLAR = 500

APARELHOS = {
    "sala": {
        "lampada_sala": 40,
        "tv_sala": 120,
        "ventilador_sala": 80,
        "console_sala": 300
    },
    "cozinha": {
        "geladeira": 150,
        "microondas": 800,
        "lampada": 60
    },
    "quarto": {
        "computador": 150,
        "lampada": 60
    },
    "banheiro": {
        "lampada": 60,
        "chuveiro": 3000
    },
    "garagem": {
        "carregador_carro": 2200,
        "lampada": 60
    }
}


categorias = list(APARELHOS.keys())
valores = list(APARELHOS.values())


