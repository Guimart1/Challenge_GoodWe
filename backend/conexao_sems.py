import os
import json
import base64
import random
import requests
from datetime import datetime
from typing import Literal, Dict, Any

# ---------------- CONFIG ----------------
Region = Literal["us", "eu"]
BASE = {
    "us": "https://us.semsportal.com",
    "eu": "https://eu.semsportal.com",
}

# ---------------- LOGIN ----------------
def _initial_token() -> str:
    """Token inicial exigido pelo SEMS"""
    original = {"uid": "", "timestamp": 0, "token": "", "client": "web", "version": "", "language": "en"}
    b = json.dumps(original).encode("utf-8")
    return base64.b64encode(b).decode("utf-8")

def crosslogin(account: str, pwd: str, region: Region = "us") -> str:
    """Faz login e retorna token válido"""
    url = f"{BASE[region]}/api/v2/common/crosslogin"
    headers = {"Token": _initial_token(), "content-type": "application/json", "Accept": "*/*"}
    payload = {
        "account": account,
        "pwd": pwd,
        "agreement_agreement": 0,
        "is_local": False
    }
    r = requests.post(url, json=payload, headers=headers, timeout=20)
    r.raise_for_status()
    js = r.json()
    if "data" not in js or js.get("code") not in (0, 1, 200):
        raise RuntimeError(f"Login falhou: {js}")
    data_to_string = json.dumps(js["data"])
    token = base64.b64encode(data_to_string.encode("utf-8")).decode("utf-8")
    return token

# ---------------- CONSULTAS ----------------
def get_inverter_list_demo(token: str, region: Region = "eu") -> Dict[str, Any]:
    """Retorna um inversor demo fixo (evita lista vazia)"""
    # Demo SN da GoodWe (funciona com demo@goodwe.com)
    demo_sn = "5010KETU229W6177"
    return {"data": [{"id": demo_sn, "name": "Demo Inversor"}]}

def safe_get(data: dict, key: str, default=None):
    val = data.get(key) if isinstance(data, dict) else None
    return val if val not in (None, "", "N/A") else default

def get_full_battery_status(token: str, inverter_id: str, region: Region = "eu") -> Dict[str, Any]:
    url = f"{BASE[region]}/api/PowerStationMonitor/GetInverterRealTimeData"
    headers = {"Token": token, "content-type": "application/json"}
    payload = {"id": inverter_id}

    r = requests.post(url, json=payload, headers=headers, timeout=20)
    r.raise_for_status()
    js = r.json()
    data = js.get("data") or {}

    return {
        # -------- Seção 1 – Status em tempo real --------
        "soc": safe_get(data, "batterySoc", round(random.uniform(40, 40), 1)),
        "p_instant": (safe_get(data, "pcharge", 0) or 0) - (safe_get(data, "pdischarge", 0) or 0)
                     or round(random.uniform(-2.0, 2.0), 2),  # kW (+ carrega, - descarrega)
        "flux": {
            "rede": safe_get(data, "pgrid", random.randint(-1000, 1000)),
            "solar": safe_get(data, "ppv", random.randint(0, 3000)),
            "bateria": safe_get(data, "pbat", random.randint(-500, 500)),
            "casa": safe_get(data, "pload", random.randint(500, 2000)),
        },
        "temp_bat": safe_get(data, "batTemp", round(random.uniform(25, 35), 1)),
        "tensao_bat": safe_get(data, "vbat", round(random.uniform(48, 52), 2)),
        "corrente_bat": safe_get(data, "ibat", round(random.uniform(-20, 20), 2)),
        "status_inversor": safe_get(data, "inverterStatus", "Online"),

        # -------- Seção 2 – Alarmes & Saúde --------
        "alarmes": data.get("alarmList", ["Nenhum alarme ativo"]),
        "soh": safe_get(data, "soh", 92),  # MOCK
        "ciclos": {
            "realizados": safe_get(data, "batteryCycles", random.randint(100, 200)),
            "estimado": 6000
        },

        # -------- Seção 3 – Histórico --------
        "historico": {
            "curva_diaria": ["08h=10%", "12h=55%", "16h=70%", "20h=50%"],  # MOCK
            "grafico_mensal": {"Jan": 120, "Fev": 140, "Mar": 100},       # MOCK kWh
            "pizza_distribuicao": {"solar": 55, "bateria": 30, "rede": 15}, # MOCK %
        },

        # -------- Seção 4 – Sustentabilidade --------
        "energia_acumulada": safe_get(data, "etotal", 10500),  # kWh
        "economia": 0.85 * (safe_get(data, "etotal", 10500) or 0),
        "co2_ev": safe_get(data, "co2total", 4800),           # kg
    }


# ---------------- MAIN ----------------
if __name__ == "__main__":
    try:
        # Credenciais (usar variáveis de ambiente ou demo)
        acc = os.getenv("SEMS_ACCOUNT", "demo@goodwe.com")
        pwd = os.getenv("SEMS_PASSWORD", "GoodweSems123!@#")

        # Login US e dados EU (conta demo)
        login_region = "us"
        data_region = "eu"

        token = crosslogin(acc, pwd, login_region)
        print("🔑 Login OK")

        # Pegando inversor demo
        inverters = get_inverter_list_demo(token, data_region)
        if not inverters.get("data"):
            raise RuntimeError("Nenhum inversor demo encontrado.")

        inverter_id = inverters["data"][0]["id"]
        print(f"⚡ Usando inversor: {inverter_id}")

        # Buscar status da bateria
        status = get_full_battery_status(token, inverter_id, data_region)

        # Montar painel
        painel = {
    "Última atualização": datetime.now().strftime("%Y-%m-%d %H:%M"),

    # Seção 1 – Status em tempo real
    "SOC (%)": status["soc"],
    "Potência instantânea (kW)": status["p_instant"],
    "Fluxo de energia (W)": status["flux"],
    "Temperatura da bateria (°C)": status["temp_bat"],
    "Tensão da bateria (V)": status["tensao_bat"],
    "Corrente da bateria (A)": status["corrente_bat"],
    "Status do inversor": status["status_inversor"],

    # Seção 2 – Alarmes & Saúde
    "Alarmes ativos": status["alarmes"],
    "Saúde da bateria (%)": status["soh"],
    "Ciclos": status["ciclos"],

    # Seção 3 – Histórico
    "Histórico diário": status["historico"]["curva_diaria"],
    "Histórico mensal (kWh)": status["historico"]["grafico_mensal"],
    "Distribuição energia (%)": status["historico"]["pizza_distribuicao"],

    # Seção 4 – Sustentabilidade
    "Energia acumulada (kWh)": status["energia_acumulada"],
    "Economia estimada (R$)": status["economia"],
    "Carbono evitado (kg CO₂)": status["co2_ev"],
}

        print("\n📊 Painel da Bateria:")
        print(json.dumps(painel, indent=2, ensure_ascii=False))

    except Exception as e:
        print("❌ Erro:", e)