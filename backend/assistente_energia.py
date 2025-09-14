import google.generativeai as genai
import simulador

genai.configure(api_key="SUA_CHAVE_GEMINI")

model = genai.GenerativeModel("gemini-1.5-flash")

dados = simulador.simular(usar_aparelho="geladeira", redirecionar_para="bateria")

if not dados:
    print("Erro ao obter dados da simulação.")
    exit()

pergunta = input("Digite sua pergunta sobre energia solar e consumo: ")

prompt = f"""
O usuário perguntou: "{pergunta}"

Aqui estão os dados da residência no momento:

- Cidade: {dados['cidade']}
- Clima atual: {dados['condicao_clima']} | {dados['temperatura']}°C
- Geração solar estimada: {dados['geracao_solar']} W
- Aparelho em uso: {dados['aparelho_usado']} (total de {dados['consumo_total']}) W
- Energia redirecionada para: {dados['redirecionamento']}
- Bateria: {dados['nivel_bateria']} Wh ({dados['bateria_soc']}% de carga)

Com base nesses dados, gere uma resposta clara, natural e útil ao usuário.
Você é um assistente inteligente de energia doméstica.
"""

try:
    resposta = model.generate_content(prompt)
    print("\nResposta da IA:\n")
    print(resposta.text)
except Exception as e:
    print("Erro ao conectar com a API Gemini:", e)