import google.generativeai as genai

genai.configure(api_key="AIzaSyBnaQ1EhiYW1XKLqVgMh742HkAI7QpK_C0")

modelo = genai.GenerativeModel("gemini-2.5-flash")

def conversar_com_ia(prompt):
    prompt_modificado = f"Responda de forma breve, direta e com no máximo 40 palavras. Pergunta {prompt}"
    resposta = modelo.generate_content(prompt_modificado)
    return resposta.text