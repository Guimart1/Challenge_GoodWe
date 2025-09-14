import os
import json
import base64
import requests
from typing import Literal, Dict, Any

Region = Literal["us", "eu"]

BASE ={
    "us": "https://us.semsportal.com",
    "eu": "https://eu.semsportal.com",
}

def _initial_token() -> str:
    original = {"uid": "", "timestamp": 0, "token": "", "client": "web", "version": "", "language": "en"}
    b = json.dumps(original).encode("utf-8")
    return base64.b64encode(b).decode("utf-8")

def crosslogin (account: str, pwd: str, region: Region = "us") -> str:
    
    url = f"{BASE[region]}/api/v2/common/crosslogin"
    headers = {"Token": _initial_token(), "content-type": "application/json", "Accept": "*/*"}
    payload = {
        "account": account,
        "pwd": pwd,
        "agreement_agreement": 0,
        "is_local": False
    }
    r = requests.post(url, json=payload, headers = headers, timeout=20)
    r.raise_for_status()
    js = r.json()
    if "data" not in js or js.get("code") not in (0, 1, 200):
        raise RuntimeError(f"Login falhou: {js}")
    data_to_string = json.dumps(js["data"])
    token = base64.b64encode(data_to_string.encode("utf-8")).decode("utf-8")
    return token

def _get_inverter_data_by_column(token: str, inv_id: str, column: str, date: str, region: Region = "eu") -> Dict[str, Any]:
    url = f"{BASE[region]}/api/PowerStationMonitor/GetInverterDataByColumn"
    headers = {"Token": token, "content-type": "application/json", "accept": "*/*"}
    payload = {"date": date, "column": column, "id": inv_id}
    r = requests.post(url, json = payload, headers = headers, timeout=20)
    r.raise_for_status()
    return r.json()

def client_from_env() -> dict[str, str]:
    acc = os.getenv("SEMS_ACCOUNT", "demo@goodwe.com")
    pwd = os.getenv("SEMS_PASSWORD", "GoodweSems123!@#")
    Region = os.getenv("SEMS_REGION", "us")
    if not acc or not pwd:
        raise RuntimeError("Defina SEMS_ACCOUNT e SEMS_PASSWORD no ambiente.")
    return {"account": acc, "password": pwd, "region": Region}

if __name__ == "__main__":
    try:
        cfg = client_from_env()
        token = crosslogin(cfg["account"], cfg["password"], cfg["region"])
        print("Login OK. Token pronto.")
    except Exception as e:
        print("Aviso:", e)
