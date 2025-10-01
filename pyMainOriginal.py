import random
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Edite .env.example com sua chave API
api_key = os.getenv("WEATHER_API_KEY")
CIDADE = 'Sao Paulo'

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
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={CIDADE}"
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
    else:
        fator_clima = 0.6

    geracao_estimada = GERACAO_MAXIMA_SOLAR * fator_clima
    return round(geracao_estimada, 2)


def simular_gestao_energia():
    dados_do_clima = obter_dados_clima()

    if not dados_do_clima:
        print("Não foi possível obter dados de clima. Encerrando simulação.")
        return

    geracao_solar_atual = calcular_geracao_solar(dados_do_clima)

    nivel_bateria = NIVEL_INICIAL_BATERIA

    print("--- Simulador de Gestão de Energia Solar ---")
    print(
        f"Clima Atual em {CIDADE}: {dados_do_clima['current']['condition']['text']} | {dados_do_clima['current']['temp_c']}°C")
    print(f"Geração Solar Estimada: {geracao_solar_atual} W")
    print("-" * 50)

    print(f"Nível Inicial da Bateria: {nivel_bateria} Wh ({round((nivel_bateria / CAPACIDADE_BATERIA) * 100)}%)")

    print("\nVocê pode ligar um dos seguintes aparelhos:")
    for nome in APARELHOS:
        print(f" - {nome.capitalize()} ({APARELHOS[nome]} W)")

    escolha = input("Digite o nome do aparelho que deseja ligar (ou 'nenhum'): ").lower()

    if escolha in APARELHOS:
        consumo_aparelhos = APARELHOS[escolha]
        print(f"\n{escolha.capitalize()} foi ligado.")
    else:
        consumo_aparelhos = 0
        print("\nNenhum aparelho foi ligado.")

    consumo_total = consumo_aparelhos + CONSUMO_STANDBY

    print(f"Consumo Total da Casa: {consumo_total} W")

    print("\nPara onde você quer redirecionar a energia? ('bateria' ou 'casa')")
    redirecionamento = input("Escolha: ").lower()

    print("\n--- Resultado da Simulação ---")

    if redirecionamento == "bateria":
        energia_para_bateria = max(0, geracao_solar_atual - consumo_total)
        novo_nivel_bateria = nivel_bateria + energia_para_bateria

        print(f"Redirecionando energia para a bateria...")
        print(f"Energia disponível para bateria: {energia_para_bateria} W")
        print(f"Nível Final da Bateria: {min(novo_nivel_bateria, CAPACIDADE_BATERIA)} Wh")

    elif redirecionamento == "casa":
        energia_necessaria_da_bateria = max(0, consumo_total - geracao_solar_atual)

        if nivel_bateria >= energia_necessaria_da_bateria:
            novo_nivel_bateria = nivel_bateria - energia_necessaria_da_bateria
            print(f"Redirecionando energia para a casa...")
            print(f"Usando {energia_necessaria_da_bateria} W da bateria para suprir o consumo.")
            print(f"Nível Final da Bateria: {novo_nivel_bateria} Wh")
        else:
            print(f"Bateria não tem energia suficiente para suprir a casa. Nível de bateria: {nivel_bateria} Wh")
            print("Será necessário usar a rede elétrica da concessionária.")
    else:
        print("Escolha inválida. A simulação não pode continuar.")


if __name__ == "__main__":
    simular_gestao_energia()
