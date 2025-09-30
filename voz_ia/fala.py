from elevenlabs.client import ElevenLabs
from io import BytesIO
import tempfile

client = ElevenLabs(api_key="sk_2a4533bd179100a2c2a5da155406d9b914264dd3723822fb")

def falar_resposta(texto):
    if not texto:
        return None
    
    audio_generator = client.text_to_speech.convert(
        text=texto,
        voice_id="EXAVITQu4vr4xnSDxMaL",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128"
    )
    audio = BytesIO()
    for chunk in audio_generator:
        audio.write(chunk)
    audio.seek(0)    
    return audio.read()