from voz_ia.voz import ouvir_microfone
from controles.controle import controlar_led
from voz_ia.fala import falar_resposta
import pygame
from io import BytesIO

def reproduzir_audio(audio_data):
    #Inicializa o pygame, carrega o áudio de um objeto BytesIO e o reproduz
    if not audio_data:
        print("Nenhum dado de áudio para reproduzir.")
        return
        
    try:
        pygame.mixer.init()
        audio_stream = BytesIO(audio_data)
        pygame.mixer.music.load(audio_stream)
        pygame.mixer.music.play()
        #Espera o áudio terminar de tocar
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        print("Áudio reproduzido com sucesso.")
    except Exception as e:
        print(f"Erro ao reproduzir áudio: {e}")
    finally:
        pygame.mixer.quit()

#Loop principal do programa
def iniciar_assistente():
    #Função principal que executa o loop do assistente
    print("Assistente iniciado. Diga 'ligar', 'desligar' ou 'parar' para sair.")
    
    while True:
        #Ouve o comando do microfone
        comando_voz = ouvir_microfone().lower()
        
        #Processa o comando recebido
        if "ligar" in comando_voz:
            print("Comando 'ligar' detectado.")
            controlar_led("ligar") #Chama a função do controle.py
            audio_resposta = falar_resposta("Ok, ligando o LED.")
            reproduzir_audio(audio_resposta)

        elif "acender" in comando_voz:
            print("Comando 'liga' detectado.")
            controlar_led("ligar") #Chama a função do controle.py
            audio_resposta = falar_resposta("Ok, ligando o LED.")
            reproduzir_audio(audio_resposta)

        elif "stop" in comando_voz:
            print("Comando 'desligar' detectado.")
            controlar_led("desligar") #Chama a função do controle.py
            audio_resposta = falar_resposta("Tudo bem, desligando o LED.")
            reproduzir_audio(audio_resposta)

        elif "desliga" in comando_voz:
            print("Comando 'desliga' detectado.")
            controlar_led("desligar") #Chama a função do controle.py
            audio_resposta = falar_resposta("Tudo bem, desligando o LED.")
            reproduzir_audio(audio_resposta)
        
        elif "parar" in comando_voz or "sair" in comando_voz:
            print("Comando 'parar' detectado. Encerrando o assistente.")
            audio_resposta = falar_resposta("Até mais!")
            reproduzir_audio(audio_resposta)
            break #Sai do loop while
        
        else:
            print(f"Comando '{comando_voz}' não reconhecido.")
            #Opcional: dar feedback de que não entendeu
            #audio_resposta = falar_resposta("Desculpe, não entendi o comando.")
            #reproduzir_audio(audio_resposta)

#Inicia o programa !!!!!!!!
#PRA INICIAR USAR "python main.py"
if __name__ == "__main__":
    iniciar_assistente()