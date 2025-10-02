# voz_bp.py

import base64
from flask import Blueprint, jsonify, request
import numpy as np
import whisper
import torch
import io
import soundfile as sf  # Precisaremos desta biblioteca para ler o áudio vindo do navegador

# Suas funções de IA
from backend.assistente_energia import conversar_com_ia
from voz_ia.fala import falar_resposta

# --- Configuração do Whisper ---
model = whisper.load_model("tiny")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# --- Criação do Blueprint ---
voz_bp = Blueprint('voz_bp', __name__)


def transcrever_audio_bytes(audio_bytes):
    """
    Recebe bytes de áudio, converte e transcreve usando o Whisper.
    """
    try:
        # O áudio do navegador geralmente vem em formato webm/ogg.
        # Usamos soundfile para ler os bytes e converter para o formato que o Whisper precisa.
        audio_data, samplerate = sf.read(io.BytesIO(audio_bytes))

        # Se o áudio for estéreo, converte para mono
        if audio_data.ndim > 1:
            audio_data = np.mean(audio_data, axis=1)

        # Converte para float32, o formato esperado pelo Whisper
        audio_data = audio_data.astype(np.float32)

        # Processamento com Whisper
        audio_data = whisper.pad_or_trim(audio_data)
        mel = whisper.log_mel_spectrogram(audio_data).to(model.device)
        options = whisper.DecodingOptions(language="pt", fp16=torch.cuda.is_available())
        result = whisper.decode(model, mel, options)

        print(f"Texto reconhecido: {result.text}")
        return result.text.strip()

    except Exception as e:
        print(f"Erro ao transcrever áudio: {e}")
        return None


@voz_bp.route('/processar-voz', methods=['POST'])
def processar_voz_route():
    if 'audio_data' not in request.files:
        return jsonify({"error": "Nenhum arquivo de áudio enviado"}), 400

    audio_file = request.files['audio_data']
    audio_bytes = audio_file.read()

    # 1. Transcrever o áudio recebido
    comando_voz = transcrever_audio_bytes(audio_bytes)
    if not comando_voz:
        return jsonify({"error": "Não foi possível entender o áudio."}), 500

    # 2. Conversar com a IA Gemini
    resposta_ia_texto = conversar_com_ia(comando_voz)

    # 3. Gerar a fala da IA com ElevenLabs
    audio_resposta_bytes = falar_resposta(resposta_ia_texto)

    # 4. Preparar o áudio para ser enviado de volta (em Base64)
    audio_resposta_b64 = base64.b64encode(audio_resposta_bytes).decode('utf-8')

    # 5. Enviar tudo de volta como JSON
    return jsonify({
        'texto_transcrito': comando_voz,
        'resposta_ia': resposta_ia_texto,
        'audio_resposta_b64': audio_resposta_b64
    })