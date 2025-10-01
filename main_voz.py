import streamlit as st
from voz_ia.voz import ouvir_microfone
from backend.assistente_energia import conversar_com_ia
from voz_ia.fala import falar_resposta
import base64
import time

st.set_page_config(page_title=" Assistente de Voz IA", layout="centered")
st.title(" Assistente de Voz com Gemini")

if st.button(" Falar com a IA"):
    comando = ouvir_microfone()
    if comando:
        st.markdown(f" **Você disse:** `{comando}`")

        resposta = conversar_com_ia(comando)
        st.markdown(f" **IA respondeu:** `{resposta}`")

        audio_bytes = falar_resposta(resposta)
        b64 = base64.b64encode(audio_bytes).decode()

        audio_html = f"""
            <audio id="audio" autoplay>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            <script>
                var audio = document.getElementById('audio');
                audio.play();
            </script>
            """
        time.sleep(1)
        st.components.v1.html(audio_html, height=0)

    else:
        st.warning("⚠️ Não consegui entender sua fala.")