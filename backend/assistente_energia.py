import google.generativeai as genai
from backend.simulador import *

genai.configure(api_key="AIzaSyA2DjYR_iz9rpho3c53JHSn3MgjIR3Pvsc")

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

def gerar_sugestao(comodo, aparelho, redirecionamento, nivel_bateria_real):
    dados = simular(comodo, aparelho, redirecionamento, nivel_bateria_real)
    ativos = [
        nome for nome in APARELHOS.get(comodo, {})
        if st.session_state.get(f"{comodo}_{nome}", False)
    ]

    if not dados:
        return None, "Erro ao obter dados da simulação."

    prompt = f"""
    Monitore o consumo de energia de uma casa, ela tem sua energia proveniente de painéis solares.
    
    Com base nos dados abaixo, sugira se o usuário deve ligar ou desligar aparelhos para otimizar o consumo de energia solar.
    Se estiver a noite a energia da bateria deve ser recomendada, mas quando alta geração solar modo de recuperação.
    De apenas sugestões de ligar ou desligar aparelhos, falando o nome do aparelho e por qual circunstancia.
    Porém se baixa energia, recomende desligar aparelhos com consumo alto e pouco uso.
    
    
    - Cidade: {dados['cidade']}
    - Clima atual: {dados['condicao_clima']} | {dados['temperatura']}°C
    - Geração solar estimada: {dados['geracao_solar']} W
    - Aparelho em uso: {dados['aparelho_usado']} ({dados['consumo_total']} W)
    - Redirecionamento: {dados['redirecionamento']}
    - Bateria: {dados['nivel_bateria']} Wh ({dados['bateria_soc']}%)
    - Dispositivos ativos no cômodo: {', '.join(ativos)}

    Seja direto, claro, evite informações com números, utilize tópicos destacando com negrito.
    """

    try:
        resposta = model.generate_content(prompt)
        return dados, resposta.text.strip()
    except Exception as e:
        return dados, f"Erro ao gerar sugestão: {e}"

def gerar_sugestao_comodo(comodo, dispositivos_ativos, dados):
    prompt = f"""
    Você é um assistente de energia doméstica.
    Analise **apenas o cômodo {comodo.upper()}** e os aparelhos ligados nele.

    Com base nos dados abaixo, sugira recomendações simples:
    - Diga quais aparelhos podem ser desligados para economizar.
    - Diga se algum deve permanecer ligado e por quê.
    - Evite números, foque em frases claras e práticas.

    Dados do cômodo:
    - Dispositivos ativos: {', '.join(dispositivos_ativos) if dispositivos_ativos else "nenhum"}
    - Consumo total do cômodo: {dados['consumo_total']} W
    - Geração solar atual: {dados['geracao_solar']} W
    - Bateria: {dados['nivel_bateria']} Wh ({dados['bateria_soc']}%)

    Responda em tópicos.
    """

    try:
        resposta = model.generate_content(prompt)
        return resposta.text.strip()
    except Exception as e:
        return f"Erro ao gerar sugestão para o cômodo: {e}"