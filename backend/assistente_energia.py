import os
import google.generativeai as genai
from dotenv import load_dotenv
from backend.core import *

load_dotenv()

# Insira sua chave em .env.example e troque o nome do arquivo para .env
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# dados = simular(usar_aparelho="geladeira", redirecionar_para="bateria")
#
# if not dados:
#     print("Erro ao obter dados da simulação.")
#     exit()
#
# pergunta = input("Digite sua pergunta sobre energia solar e consumo: ")
#
# prompt = f"""
# O usuário perguntou: "{pergunta}"
#
# Aqui estão os dados da residência no momento:
#
# - Cidade: {dados['cidade']}
# - Clima atual: {dados['condicao_clima']} | {dados['temperatura']}°C
# - Geração solar estimada: {dados['geracao_solar']} W
# - Aparelho em uso: {dados['aparelho_usado']} (total de {dados['consumo_total']}) W
# - Energia redirecionada para: {dados['redirecionamento']}
# - Bateria: {dados['nivel_bateria']} Wh ({dados['bateria_soc']}% de carga)
#
# Com base nesses dados, gere uma resposta clara, natural e útil ao usuário.
# Você é um assistente inteligente de energia doméstica.
# """
#
# try:
#     resposta = model.generate_content(prompt)
#     print("\nResposta da IA:\n")
#     print(resposta.text)
# except Exception as e:
#     print("Erro ao conectar com a API Gemini:", e)

def gerar_sugestao(dados_simulacao, dispositivos_ativos):
    """
    Gera uma sugestão de otimização de energia com base nos dados da simulação.

    Args:
        dados_simulacao (dict): Dados da simulação obtidos da função simular().
        dispositivos_ativos (list): Lista de nomes dos dispositivos ligados.

    Returns:
        tuple: (dict de dados, str de resposta) ou (dict de dados, str de erro)
    """
    if not dados_simulacao:
        return None, "Erro ao obter dados da simulação."

    # Lógica para determinar o estado da energia com base nos dados.
    # Isso torna as instruções para a IA mais diretas e elimina a necessidade de números no prompt.
    if dados_simulacao['geracao_solar'] > 400:
        geracao_solar_status = "alta"
    elif dados_simulacao['geracao_solar'] > 150:
        geracao_solar_status = "moderada"
    else:
        geracao_solar_status = "baixa"

    if dados_simulacao['bateria_soc'] > 80:
        bateria_status = "carga excelente"
    elif dados_simulacao['bateria_soc'] > 40:
        bateria_status = "carga boa"
    else:
        bateria_status = "carga baixa"

    prompt = f"""
    Você é um assistente de energia doméstica focado em eficiência.
    Sua única tarefa é dar sugestões para ligar ou desligar aparelhos.

    Instruções estritas para a resposta:
    - NUNCA USE NÚMEROS na sua resposta, de forma alguma. Use apenas termos como "alta", "baixa" ou "boa".
    - Use tópicos com um hífen (-) e negrito para destacar os aparelhos. Use tópicos para cada um dos aparelhos.
    - Baseie suas sugestões nos seguintes dados, mas deixe os ocultos:
        - Geração solar: {geracao_solar_status}
        - Bateria: {bateria_status}
        - Dispositivos ativos: {', '.join(dispositivos_ativos) if dispositivos_ativos else 'nenhum'}
        - Clima: {dados_simulacao['condicao_clima']}

    Siga essas regras de forma rigorosa.
    """
    try:
        resposta = model.generate_content(prompt)
        resposta_visual = resposta.text.strip()
        return resposta_visual
    except Exception as e:
        return f"Erro ao gerar sugestão: {e}"


def gerar_sugestao_comodo(comodo, dados_comodo, dispositivos_ativos):
    """
    Gera uma sugestão de otimização de energia para um cômodo específico.

    Args:
        comodo (str): Nome do cômodo a ser analisado.
        dados_comodo (dict): Dicionário com consumo, geração solar e dados da bateria.
        dispositivos_ativos (list): Lista de nomes dos dispositivos ligados no cômodo.

    Returns:
        str: Resposta da IA com sugestões ou mensagem de erro.
    """
    prompt = f"""
    Você é um assistente de energia doméstica.
    Analise **apenas o cômodo {comodo.upper()}** e os aparelhos ligados nele.

    Com base nos dados abaixo, sugira recomendações simples:
    - Diga quais aparelhos podem ser desligados para economizar.
    - Diga se algum deve permanecer ligado e por quê.
    - Evite números, foque em frases claras e práticas.

    Dados do cômodo:
    - Dispositivos ativos: {', '.join(dispositivos_ativos) if dispositivos_ativos else "nenhum"}
    - Consumo total do cômodo: {dados_comodo['consumo_total']} W
    - Geração solar atual: {dados_comodo['geracao_solar']} W
    - Bateria: {dados_comodo['nivel_bateria']} Wh ({dados_comodo['bateria_soc']}%)

    Responda em tópicos.
    """

    try:
        resposta = model.generate_content(prompt)
        # Remove os caracteres de formatação Markdown da resposta da IA.
        resposta_limpa = resposta.text.strip().replace('**', '').replace('*', '').replace('-', '')
        return resposta_limpa
    except Exception as e:
        return f"Erro ao gerar sugestão para o cômodo: {e}"

def conversar_com_ia(prompt):
    prompt_modificado = f"Responda de forma breve, direta e com no máximo 40 palavras. Pergunta: {prompt}"
    resposta = model.generate_content(prompt_modificado)
    return resposta.text