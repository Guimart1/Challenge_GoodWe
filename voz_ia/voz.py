import sounddevice as sd
import numpy as np
import whisper
import torch

model = whisper.load_model("tiny")

DURACAO = 5
TAXA = 16000

def ouvir_microfone():
    print("Gravando... Fale agora.")
    audio = sd.rec(int(DURACAO * 16000), samplerate=16000, channels=1, dtype='int16')
    sd.wait()
    print("Gravação finalizada.")

    audio = audio.flatten().astype(np.float32) / 32768.0

    audio = whisper.pad_or_trim(audio)

    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    options = whisper.DecodingOptions(language="pt", fp16=torch.cuda.is_available())
    result = whisper.decode(model, mel, options)

    print(f"Texto reconhecido: {result.text}")
    return result.text.strip()