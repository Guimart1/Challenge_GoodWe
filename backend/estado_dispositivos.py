import streamlit as st
from backend.config import APARELHOS

import streamlit as st

def toggle_dispositivo(comodo, chave):
    chave_unica = f"{comodo}_{chave}"

    # Usa diretamente o session_state do widget
    return st.checkbox(
        chave.replace("_", " ").upper(),
        value=st.session_state.get(chave_unica, False),
        key=chave_unica
    )

def get_dispositivos_ativos(comodo):
    return [
        chave for chave in APARELHOS[comodo]
        if st.session_state.get(f"{comodo}_{chave}", False)
    ]