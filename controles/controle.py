import logging
import socket
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Insira suas chaves em .env.example e troque o nome do arquivo para .env
ACCESS_ID = os.getenv("ACCESS_ID")
ACCESS_KEY = os.getenv("ACCESS_KEY")
API_ENDPOINT = os.getenv("API_ENDPOINT")
DEVICE_ID = os.getenv("DEVICE_ID")

# Função para retornar a mudança do DNS
_original_getaddrinfo = socket.getaddrinfo

def _ipv4_getaddrinfo(*args, **kwargs):
    # Força a resolução de DNS para retornar apenas endereços IPv4
    responses = _original_getaddrinfo(*args, **kwargs)
    return [res for res in responses if res[0] == socket.AF_INET]

socket.getaddrinfo = _ipv4_getaddrinfo

# Enable debug log (se quiser debugar)
#TUYA_LOGGER.setLevel(logging.DEBUG)

#Init OpenAPI and connect
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

# Função para ligar ou desligar o dispositivo
def controlar_led(comando: str):
    match comando.lower():
        case "ligar":
            valor = True
        case "desligar":
            valor = False
        case _:
            print("Comando inválido. Use 'ligar' ou 'desligar'.")
            return
    
    commands = {'commands': [{'code': 'switch_led', 'value': valor}]}
    print(f"Enviando comando para {comando} o LED...")
    response = openapi.post(f"/v1.0/iot-03/devices/{DEVICE_ID}/commands", commands)
    print("Resposta da API:", response)


# Exemplo de uso:
#controlar_led("ligar")     # Liga o LED
#controlar_led("desligar")  # Desliga o LED
