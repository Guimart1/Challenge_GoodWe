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

# backend/assistente_energia.py

def gerar_sugestao(dados_simulacao, dispositivos_ativos):
    """
    Gera uma sugestão de otimização de energia em um formato de texto específico.
    """
    if not dados_simulacao:
        return "Erro ao obter dados da simulação."

    # A lógica de status continua a mesma
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

    # --- PROMPT MODIFICADO PARA GERAR TEXTO FORMATADO ---
    prompt = f"""
    Analise os dados de energia e retorne uma resposta em texto simples, seguindo o formato obrigatório abaixo.

    Dados de entrada (use para basear sua resposta, mas não os mostre):
    - Geração solar: {geracao_solar_status}
    - Bateria: {bateria_status}
    - Dispositivos ativos: {', '.join(dispositivos_ativos) if dispositivos_ativos else 'nenhum'}
    - Clima: {dados_simulacao['condicao_clima']}

    FORMATO DE SAÍDA:
    [Frase resumindo o consumo atual da casa]
    [Tópicos de aparelhos para desligar, se consumo estiver alto, bateria baixa]
    [Frase resumindo clima e geração]
    - Regras de consumo geral: até 1000W = baixo; de 1000 até 2500w = médio, de 3000 para cima = Alto. 
    Se o nível estiver alto, faça sugestões para desligar aparelhos que mais estão consumindo.
    """

    try:
        resposta = model.generate_content(prompt)
        return resposta.text.strip()
    except Exception as e:
        return f"Erro ao gerar sugestão: {e}"


def gerar_sugestao_comodo(comodo, dados_comodo, dispositivos_ativos, dados_globais, dispositivos_disponiveis):
    """
    Gera uma sugestão para um cômodo, focando na relação entre consumo e nível da bateria.
    """
    # A lógica de status continua a mesma
    if dados_globais['geracao_solar'] > 400:
        geracao_solar_status = "alta"
    elif dados_globais['geracao_solar'] > 150:
        geracao_solar_status = "moderada"
    else:
        geracao_solar_status = "baixa"

    if dados_globais['soc_bateria'] > 80:
        bateria_status = "carga excelente"
    elif dados_globais['soc_bateria'] >= 40:
        bateria_status = "carga boa"
    else:
        bateria_status = "carga baixa"

    # --- PROMPT ATUALIZADO COM NOVA LÓGICA ---
    prompt = f"""
    Você é um sistema lógico de gerenciamento de energia. Sua tarefa é analisar os dados e retornar APENAS o texto no formato especificado, sem conversas.
    O princípio mais importante é o equilíbrio entre o CONSUMO TOTAL e o NÍVEL DA BATERIA.

    **DADOS GLOBAIS DA CASA:**
    - Geração Solar: {geracao_solar_status}
    - Nível da Bateria: {bateria_status}
    - Consumo Total da Casa: {dados_globais['consumo_total']} W

    **DADOS DO CÔMODO ATUAL: "{comodo.upper()}"**
    - Dispositivos Disponíveis: {', '.join(dispositivos_disponiveis) if dispositivos_disponiveis else "nenhum"}
    - Dispositivos Ativos Agora: {', '.join(dispositivos_ativos) if dispositivos_ativos else "nenhum"}

    **FORMATO DE SAÍDA OBRIGATÓRIO:**
    Sugestões para {comodo.title()}:
    - "Nome do Aparelho": ligar/desligar
    (Se não houver sugestões, escreva: Nenhuma ação recomendada neste cômodo.)

    Resumo Geral da Casa:
    - [Escreva aqui uma única frase resumindo o estado energético e uma recomendação geral]

    **REGRAS ESTRITAS DE DECISÃO:**
    1.  **CENÁRIO DE ALERTA (Bateria Baixa):** Se o `Nível da Bateria` for 'carga baixa', sugira DESLIGAR aparelhos de alto consumo que estejam ativos no cômodo.
    2.  **CENÁRIO DE OPORTUNIDADE (Excedente de Energia):** Se o `Nível da Bateria` for 'carga excelente' E a `Geração Solar` for 'alta', sugira LIGAR um aparelho útil da lista de 'Dispositivos Disponíveis' que esteja desligado.
    3.  **CENÁRIO DE OTIMIZAÇÃO (Consumo Alto):** Se o `Consumo Total da Casa` for maior que 2000W e a `Geração Solar` não for 'alta', sugira DESLIGAR aparelhos não essenciais no cômodo para aliviar a carga.
    4.  **REGRA DE OURO:** NUNCA sugira uma ação para um aparelho que já está nesse estado (não sugira "ligar" algo que já está ativo).
    5.  Siga o formato de saída RIGOROSAMENTE.
    """
    try:
        resposta = model.generate_content(prompt)
        return resposta.text.strip()
    except Exception as e:
        return f"Erro ao gerar sugestão para o cômodo: {e}"



def conversar_com_ia(prompt):
    prompt_modificado = f"""
    Responda de forma breve, direta e com no máximo 40 palavras.
    Pergunta: {prompt}"""

    resposta = model.generate_content(prompt_modificado)
    return resposta.text