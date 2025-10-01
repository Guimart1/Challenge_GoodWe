from elevenlabs.client import ElevenLabs
from io import BytesIO
import os

# Edite .env.example com sua chave API
elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")

def falar_resposta(texto):
    if not texto:
        return None
    
    client = ElevenLabs(api_key=elevenlabs_key)
    
    audio_generator = client.text_to_speech.convert(
        text=texto,
        voice_id="EXAVITQu4vr4xnSDxMaL",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
        optimize_streaming_latency=1
    )
    audio = BytesIO()
    for chunk in audio_generator:
        audio.write(chunk)
    audio.seek(0)    
    return audio.read()