# blueprints/voz_bp.py

import base64
from flask import Blueprint, jsonify, request, session
import whisper
import torch
import tempfile
import os

from backend.assistente_energia import conversar_com_ia
from voz_ia.fala import falar_resposta
from controles.controle import controlar_led  # Importa o controle do LED

model = whisper.load_model("small")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

voz_bp = Blueprint('voz_bp', __name__)

COMODO_LED = "sala"
DISPOSITIVO_LED = "lampada_sala"

def transcrever_audio_bytes(audio_bytes):
    temp_file = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
            temp.write(audio_bytes)
            temp_file = temp.name

        audio = whisper.load_audio(temp_file)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        options = whisper.DecodingOptions(language="pt", fp16=torch.cuda.is_available())
        result = whisper.decode(model, mel, options)

        return result.text.strip()
    except Exception as e:
        print(f"ERRO DURANTE TRANSCRIÇÃO: {e}")
        return None
    finally:
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)


@voz_bp.route('/processar-voz', methods=['POST'])
def processar_voz_route():
    if 'audio_data' not in request.files:
        return jsonify({"error": "Nenhum arquivo de áudio enviado"}), 400

    audio_file = request.files['audio_data']
    audio_bytes = audio_file.read()

    comando_voz = transcrever_audio_bytes(audio_bytes)
    if not comando_voz or len(comando_voz.strip()) < 1:
        return jsonify({"error": "Não foi possível entender o áudio."}), 400

    comando_voz_lower = comando_voz.lower()

    # Inicializa sessão caso não exista
    if "dispositivos_estado" not in session:
        session["dispositivos_estado"] = {}
    if COMODO_LED not in session["dispositivos_estado"]:
        session["dispositivos_estado"][COMODO_LED] = {}
    if DISPOSITIVO_LED not in session["dispositivos_estado"][COMODO_LED]:
        session["dispositivos_estado"][COMODO_LED][DISPOSITIVO_LED] = False

    # Detecta comandos de ligar/desligar
    if any(palavra in comando_voz_lower for palavra in ["liga", "ligar", "ligue", "acender"]):
        controlar_led("ligar")
        session["dispositivos_estado"][COMODO_LED][DISPOSITIVO_LED] = True
        resposta_texto = "Ok, ligando a lâmpada da sala."
    elif any(palavra in comando_voz_lower for palavra in ["desliga", "desligar", "desligue", "apagar"]):
        controlar_led("desligar")
        session["dispositivos_estado"][COMODO_LED][DISPOSITIVO_LED] = False
        resposta_texto = "Tudo bem, desligando a lâmpada da sala."
    else:
        # Caso não seja um comando físico, apenas conversa com a IA
        resposta_texto = conversar_com_ia(comando_voz)

    session.modified = True  # Importante para o Flask atualizar a sessão

    # Gera áudio da resposta
    audio_resposta_bytes = falar_resposta(resposta_texto)
    audio_resposta_b64 = base64.b64encode(audio_resposta_bytes).decode('utf-8') if audio_resposta_bytes else ''

    return jsonify({
        'texto_transcrito': comando_voz,
        'resposta_ia': resposta_texto,
        'audio_resposta_b64': audio_resposta_b64,
        'refresh_page': True
    })
