# blueprints/gerenciamento.py
from flask import Blueprint, render_template, session, request, redirect, url_for
import requests

from backend.config import APARELHOS, CONSUMO_STANDBY, CAPACIDADE_BATERIA
from backend.assistente_energia import gerar_sugestao_comodo
from backend.core import get_sems_token, get_battery_status, simular

gerenciamento_bp = Blueprint('gerenciamento', __name__)


@gerenciamento_bp.route('/gerenciamento')
def index():
    # --- ADIÇÃO: Dicionário de Ícones ---
    # Mapeia o nome do cômodo (como está em APARELHOS) para a URL do ícone.
    icones_comodos = {
        "sala": "https://cdn-icons-png.flaticon.com/512/1010/1010398.png",
        "cozinha": "https://cdn-icons-png.flaticon.com/512/3565/3565450.png",
        "quarto": "https://img.icons8.com/?size=100&id=8021&format=png&color=000000",
        "banheiro": "https://img.icons8.com/?size=100&id=9141&format=png&color=000000",
        "garagem": "https://img.icons8.com/?size=100&id=1625&format=png&color=000000"
    }
    icon_lightning = "https://static.thenounproject.com/png/2039810-200.png"
    comodo_selecionado = session.get("comodo_selecionado", "sala")

    # Lógica de cálculo (mesma do seu container_gerenciamento)
    consumo_total = CONSUMO_STANDBY
    dispositivos_ativos = []
    for comodo, dispositivos in session["dispositivos_estado"].items():
        for chave, ligado in dispositivos.items():
            if ligado:
                consumo_total += APARELHOS.get(comodo, {}).get(chave, 0)
                if comodo == comodo_selecionado:
                    dispositivos_ativos.append(chave.replace("_", " ").title())

    # Busca de dados
    try:
        token = get_sems_token()
        status_bateria = get_battery_status(token)
        soc_bateria = status_bateria.get("soc", 0) if status_bateria else 0
        nivel_bateria_real = CAPACIDADE_BATERIA * (soc_bateria / 100)
        dados_simulacao = simular(comodo_selecionado, "", "", nivel_bateria_real)
        sugestao_comodo = gerar_sugestao_comodo(comodo_selecionado, dados_simulacao, dispositivos_ativos)
    except Exception as e:
        soc_bateria = 10
        nivel_bateria_real = CAPACIDADE_BATERIA * (soc_bateria / 100)
        sugestao_comodo = f"Não foi possível obter dados. Erro: {e}"

    # Cálculo de tempo restante
    if consumo_total > CONSUMO_STANDBY and nivel_bateria_real > 0:
        tempo_restante_horas = nivel_bateria_real / consumo_total
        horas = int(tempo_restante_horas)
        minutos = int((tempo_restante_horas * 60) % 60)
        tempo_restante_formatado = f"~ {horas}h {minutos}m"
    elif consumo_total <= CONSUMO_STANDBY:
        tempo_restante_formatado = "Apenas Standby"
    else:
        tempo_restante_formatado = "Bateria Esgotada"

    return render_template('gerenciamento.html',
                           active_page='gerenciamento',
                           comodos=APARELHOS.keys(),
                           comodo_selecionado=comodo_selecionado,
                           icon_lightning=icon_lightning,
                           icones_comodos=icones_comodos,
                           dispositivos_no_comodo=APARELHOS.get(comodo_selecionado, {}),
                           dispositivos_estado=session["dispositivos_estado"],
                           sugestao_comodo=sugestao_comodo,
                           soc_bateria=soc_bateria,
                           consumo_total=consumo_total,
                           tempo_restante_formatado=tempo_restante_formatado)


@gerenciamento_bp.route('/gerenciamento/select_comodo', methods=['POST'])
def select_comodo():
    comodo = request.form.get('comodo')
    if comodo in APARELHOS:
        session['comodo_selecionado'] = comodo
    return redirect(url_for('gerenciamento.index'))


@gerenciamento_bp.route('/gerenciamento/toggle_device', methods=['POST'])
def toggle_device():
    comodo = request.form.get('comodo')
    device = request.form.get('device')

    # Atualiza o estado na sessão
    if comodo and device and comodo in session['dispositivos_estado'] and device in session['dispositivos_estado'][
        comodo]:
        session['dispositivos_estado'][comodo][device] = not session['dispositivos_estado'][comodo][device]
        session.modified = True  # Informa ao Flask que a sessão foi alterada

    return redirect(url_for('gerenciamento.index'))