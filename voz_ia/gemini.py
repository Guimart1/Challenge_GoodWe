import google.generativeai as genai

genai.configure(api_key="AIzaSyBnaQ1EhiYW1XKLqVgMh742HkAI7QpK_C0")

modelo = genai.GenerativeModel("gemini-2.5-flash")

def conversar_com_ia(prompt):
    resposta = modelo.generate_content(prompt)
    return resposta.text