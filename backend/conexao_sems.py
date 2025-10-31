import os
import json
import random
from datetime import datetime
from typing import Dict, Any

# ---------------- CONFIG SIMULADA ----------------
# Não há mais necessidade de URLs de API ou regiões

def mock_login(account: str, pwd: str) -> str:
    """
    Função de login simulada.
    Não faz nenhuma chamada de rede, apenas retorna um token falso para manter a estrutura do código.
    """
    print(f"Simulando login para: {account}...")
    return "TOKEN_SIMULADO_COM_SUCESSO"

def get_mock_inverter_list() -> Dict[str, Any]:
    """
    Retorna uma lista de inversores simulada com um ID fixo.
    """
    return {
        "data": [{"id": "GW-MOCK-SN-12345", "name": "Inversor Simulado"}]
    }

def get_mock_full_battery_status(inverter_id: str) -> Dict[str, Any]:
    """
    Gera um status completo e fiel da bateria, simulando o comportamento
    de um sistema fotovoltaico real com base na hora do dia.
    """
    agora = datetime.now()
    hora_atual = agora.hour

    # --- LÓGICA DE SIMULAÇÃO BASEADA NA HORA DO DIA ---

    # 1. Geração Solar (ppv) - Curva senoidal simulada
    if 6 <= hora_atual < 12: # Manhã (rampa de subida)
        fator = (hora_atual - 6) / 6
        ppv = int(3500 * fator) + random.randint(-100, 100)
    elif 12 <= hora_atual < 18: # Tarde (pico e rampa de descida)
        fator = (18 - hora_atual) / 6
        ppv = int(3500 * fator) + random.randint(-100, 100)
    else: # Noite
        ppv = 0

    # 2. Consumo da Casa (pload) - Varia com o horário de pico
    if 5 <= hora_atual < 9: # Manhã (pico)
        pload = random.randint(800, 1500)
    elif 18 <= hora_atual < 22: # Noite (pico principal)
        pload = random.randint(1000, 2500)
    else: # Consumo base
        pload = random.randint(200, 500)

    # 3. Lógica da Bateria (pbat e soc)
    saldo_energia = ppv - pload  # Saldo: Geração - Consumo
    
    soc = 80 # SOC base para o cálculo
    pbat = 0
    pgrid = 0
    inverter_status = "Standby"

    if saldo_energia > 0: # Excedente de energia (Dia com Sol)
        inverter_status = "Online"
        # Tenta carregar a bateria com o excedente, limitado a 2500W
        pbat = min(saldo_energia, 2500)
        soc = min(100, soc + (pbat / 5000) * 100) # Simula ganho de SOC
        
        # O que sobrar depois de carregar a bateria, exporta para a rede
        pgrid = (saldo_energia - pbat) * -1 # Negativo = Exportando

    elif saldo_energia < 0: # Déficit de energia (Noite ou Dia Nublado)
        inverter_status = "Online"
        deficit = abs(saldo_energia)
        
        # Tenta suprir o déficit com a bateria, limitado a 2500W
        pbat = -min(deficit, 2500)
        soc = max(15, soc - (abs(pbat) / 5000) * 100) # Simula perda de SOC
        
        # Se a bateria não for suficiente, importa da rede
        if abs(pbat) < deficit:
            pgrid = deficit - abs(pbat) # Positivo = Importando

    # Ajustes finais para realismo
    soc = round(soc, 1)
    temp_bat = round(25 + (abs(pbat) / 2500) * 5, 1) # Bateria esquenta um pouco com uso intenso
    vbat = round(48.0 + (soc - 50) / 25, 2) # Tensão varia com o SOC
    ibat = round(pbat / vbat, 2)

    return {
        # -------- Seção 1 – Status em tempo real (SIMULADO) --------
        "soc": soc,
        "p_instant": round(pbat / 1000, 2), # kW (+ carrega, - descarrega)
        "flux": {
            "rede": pgrid,
            "solar": ppv,
            "bateria": pbat,
            "casa": pload,
        },
        "temp_bat": temp_bat,
        "tensao_bat": vbat,
        "corrente_bat": ibat,
        "status_inversor": inverter_status,

        # -------- Seção 2 – Alarmes & Saúde (Valores fixos críveis) --------
        "alarmes": ["Nenhum alarme ativo"],
        "soh": 98,
        "ciclos": {
            "realizados": 342,
            "estimado": 6000
        },

        # -------- Seção 3 – Histórico (Valores fixos críveis) --------
        "historico": {
            "curva_diaria": ["08h=10%", "12h=55%", "16h=70%", "20h=50%"],
            "grafico_mensal": {"Jan": 320, "Fev": 340, "Mar": 310},
            "pizza_distribuicao": {"solar": 65, "bateria": 25, "rede": 10},
        },

        # -------- Seção 4 – Sustentabilidade (Valores fixos críveis) --------
        "energia_acumulada": 12540,
        "economia": 0.85 * 12540,
        "co2_ev": 5120,
    }


# ---------------- MAIN ----------------
if __name__ == "__main__":
    try:
        # Credenciais não são mais usadas para a API, mas mantidas para a estrutura
        acc = os.getenv("SEMS_ACCOUNT", "seu_email@ficticio.com")
        pwd = os.getenv("SEMS_PASSWORD", "SuaSenhaFicticia")

        # Login simulado
        token = mock_login(acc, pwd)
        print("🔑 Login simulado OK")

        # Pegando inversor simulado
        inverters = get_mock_inverter_list()
        inverter_id = inverters["data"][0]["id"]
        print(f"⚡ Usando inversor simulado: {inverter_id}")

        # Buscar status simulado da bateria
        status = get_mock_full_battery_status(inverter_id)

        # Montar painel
        painel = {
            "Última atualização": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "MODO": "DADOS SIMULADOS",
            "Status do inversor": status["status_inversor"],
            "SOC (%)": status["soc"],
            "Potência da Bateria (kW)": status["p_instant"],
            "Fluxo de Energia (W)": status["flux"],
            "Temperatura da Bateria (°C)": status["temp_bat"],
            "Tensão da Bateria (V)": status["tensao_bat"],
            "Corrente da Bateria (A)": status["corrente_bat"],
            "Saúde da Bateria (SoH %)": status["soh"],
            "Ciclos": status["ciclos"],
            "Economia Estimada (R$)": f'{status["economia"]:.2f}',
            "Carbono Evitado (kg CO₂)": status["co2_ev"],
        }

        print("\n📊 Painel Simulado da Bateria:")
        print(json.dumps(painel, indent=2, ensure_ascii=False))

    except Exception as e:
        print("❌ Erro inesperado no script:", e)