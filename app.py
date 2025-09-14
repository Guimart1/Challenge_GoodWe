import streamlit as st
from telas.inicio import container1, container2
from telas.bateria import container_bateria
from telas.painel_solar import container_painel
from telas.gerenciamento import container_gerenciamento
from components import sidebar
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Gestão de Energia", layout="wide")

st_autorefresh(interval=5000, limit=None, key="refresh")


 # Mesmo sem retorno, isso desenha a sidebar
pagina = st.query_params.get("page", "Ínicio")
sidebar(pagina)

if pagina == "Ínicio":
    container1()
    container2()
elif pagina == "Bateria":
    container_bateria()
elif pagina == "Gerenciamento":
    container_gerenciamento()
elif pagina == "Painel Solar":
    container_painel()



