# voz_ia/fala.py

from elevenlabs.client import ElevenLabs
from io import BytesIO
import os

elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")


def falar_resposta(texto):
    if not elevenlabs_key:
        print("DEBUG: ERRO - Chave ELEVENLABS_API_KEY não encontrada.")
        return None
    if not texto or not texto.strip():
        print("DEBUG: Texto para fala está vazio.")
        return None

    try:
        client = ElevenLabs(api_key=elevenlabs_key)
        print(f"DEBUG: Enviando texto para ElevenLabs: '{texto}'")
        audio_generator = client.text_to_speech.convert(
            text=texto,
            voice_id="EXAVITQu4vr4xnSDxMaL",
            model_id="eleven_multilingual_v2"
        )

        audio_bytes_io = BytesIO()
        for chunk in audio_generator:
            audio_bytes_io.write(chunk)

        audio_bytes_io.seek(0)
        audio_final = audio_bytes_io.read()

        if not audio_final:
            print("DEBUG: ERRO - ElevenLabs retornou áudio vazio.")
            return None

        print(f"DEBUG: ElevenLabs retornou {len(audio_final)} bytes.")
        return audio_final

    except Exception as e:
        print(f"DEBUG: Um erro inesperado ocorreu em 'falar_resposta': {e}")
        return None