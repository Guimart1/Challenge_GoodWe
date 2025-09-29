import streamlit as st

def interpretar_comando(texto):
    texto = texto.lower()

    if "ligar luz" in texto:
        st.success("Luz ligada.")
        return True
    
    elif "desligar luz" in texto:
        st.warning("Luz desligada.")
        return True
    
    elif "abrir janela" in texto:
        st.info("Janela aberta.")
        return True
    
    return False