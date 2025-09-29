import speech_recognition as sr

def ouvir_microfone():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ouvindo...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio, language="pt-BR")
    except:
        return None    