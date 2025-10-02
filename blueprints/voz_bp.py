# blueprints/voz_bp.py

import base64
from flask import Blueprint, jsonify, request
import numpy as np
import whisper
import torch
import io
import os
import tempfile

from backend.assistente_energia import conversar_com_ia
from voz_ia.fala import falar_resposta

# Carregar modelo Whisper (usando "small" para boa precisão)
model = whisper.load_model("small")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

voz_bp = Blueprint('voz_bp', __name__)


def transcrever_audio_bytes(audio_bytes):
    """
    Transcreve um bloco de bytes de áudio para texto usando Whisper.
    Usa um arquivo temporário para garantir a leitura mais estável do áudio.
    """
    temp_file = None
    try:
        # Cria um arquivo temporário de forma segura
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

    if not comando_voz or len(comando_voz.strip()) < 4:
        return jsonify({"error": "Não foi possível entender o áudio com clareza."}), 400

    resposta_ia_texto = conversar_com_ia(comando_voz)
    audio_resposta_bytes = falar_resposta(resposta_ia_texto)

    if not audio_resposta_bytes:
        return jsonify({
            'texto_transcrito': comando_voz,
            'resposta_ia': resposta_ia_texto,
            'audio_resposta_b64': ''
        })

    audio_resposta_b64 = base64.b64encode(audio_resposta_bytes).decode('utf-8')
    return jsonify({
        'texto_transcrito': comando_voz,
        'resposta_ia': resposta_ia_texto,
        'audio_resposta_b64': audio_resposta_b64
    })