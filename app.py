import streamlit as st
from backend import obter_dados_clima, calcular_geracao_solar
<<<<<<< HEAD
from frontend import sidebar
=======
from frontend import sidebar, container1
>>>>>>> ec57396a99d8f608a2d1947221416d1dd5540158
from config import NIVEL_INICIAL_BATERIA, CAPACIDADE_BATERIA, CONSUMO_STANDBY, APARELHOS

st.set_page_config(page_title="Gestão de Energia", layout="wide")

sidebar()

dados = obter_dados_clima()
if not dados:
    st.error("Erro ao obter dados de clima.")
    st.stop()

<<<<<<< HEAD
=======
container1()

>>>>>>> ec57396a99d8f608a2d1947221416d1dd5540158
geracao = calcular_geracao_solar(dados)
st.write(f"**Clima:** {dados['current']['condition']['text']} | {dados['current']['temp_c']}°C")
st.write(f"**Geração Solar Estimada:** {geracao} W")


aparelho = st.selectbox("Escolha um aparelho:", ["nenhum"] + list(APARELHOS.keys()))
consumo = APARELHOS.get(aparelho, 0) + CONSUMO_STANDBY
st.write(f"**Consumo Total:** {consumo} W")

redirecionamento = st.radio("Redirecionar energia para:", ["bateria", "casa"])
nivel_bateria = NIVEL_INICIAL_BATERIA

if redirecionamento == "bateria":
    energia_para_bateria = max(0, geracao - consumo)
    novo_nivel = min(nivel_bateria + energia_para_bateria, CAPACIDADE_BATERIA)
    st.success(f"🔋 Energia para bateria: {energia_para_bateria} W | Nível final: {novo_nivel} Wh")
else:
    energia_necessaria = max(0, consumo - geracao)
    if nivel_bateria >= energia_necessaria:
        novo_nivel = nivel_bateria - energia_necessaria
        st.success(f"🏠 Energia da bateria usada: {energia_necessaria} W | Nível final: {novo_nivel} Wh")
    else:
        st.warning("⚠️ Bateria insuficiente. Usando rede elétrica.")


<<<<<<< HEAD
=======

>>>>>>> ec57396a99d8f608a2d1947221416d1dd5540158
