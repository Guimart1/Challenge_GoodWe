import streamlit as st
from telas.inicio import container_inicio
from telas.bateria import container_bateria
from telas.painel_solar import container_painel
from telas.gerenciamento import container_gerenciamento
from components import sidebar
from streamlit_autorefresh import st_autorefresh
from backend.assistente_energia import gerar_sugestao

st.set_page_config(page_title="Gestão de Energia", layout="wide")


pagina = st.query_params.get("page", "Ínicio")
sidebar(pagina)
if pagina == "Ínicio":
    container_inicio()
elif pagina == "Bateria":
    container_bateria()
elif pagina == "Gerenciamento":
    container_gerenciamento()
elif pagina == "Painel Solar":
    container_painel()



