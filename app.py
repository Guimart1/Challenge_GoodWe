import streamlit as st
from backend import obter_dados_clima, calcular_geracao_solar
from frontend import sidebar,container1, container2
from config import NIVEL_INICIAL_BATERIA, CAPACIDADE_BATERIA, CONSUMO_STANDBY, APARELHOS
from streamlit_autorefresh import st_autorefresh
st.set_page_config(page_title="Gestão de Energia", layout="wide")

st_autorefresh(interval=5000, limit=None, key="refresh")

sidebar()

container1()

container2()

