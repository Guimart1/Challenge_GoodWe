# blueprints/inicio.py

# CORREÇÃO 1: Importar o 'session' do Flask
from flask import Blueprint, render_template, session
from datetime import datetime
import pandas as pd
import plotly.express as px

# Importa as funções do backend
from backend.core import get_sems_token, get_battery_status, simular
from backend.assistente_energia import gerar_sugestao
from backend.config import CAPACIDADE_BATERIA, APARELHOS

# Cria o Blueprint
inicio_bp = Blueprint('inicio', __name__)


# --- Funções de ajuda (convertidas de 'elementos_tela.py') ---

# CORREÇÃO 2: Implementação completa da função de ícone do clima
def get_clima_icon_html(condicao):
    hora = datetime.now().hour
    esta_de_noite = hora < 6 or hora >= 18

    icones = {
        "Céu limpo": '<img width="110" height="110" src="https://img.icons8.com/external-tanah-basah-basic-outline-tanah-basah/96/external-sun-summer-tanah-basah-basic-outline-tanah-basah.png"/>',
        "Sol": '<img width="110" height="110" src="https://img.icons8.com/external-tanah-basah-basic-outline-tanah-basah/96/external-sun-summer-tanah-basah-basic-outline-tanah-basah.png"/>',
        "Encoberto": '<img width="110" height="110" src="https://img.icons8.com/ios/100/cloud--v1.png"/>',
        "Parcialmente nublado": '<img width="110" height="110" src="https://img.icons8.com/ios/100/partly-cloudy-day--v1.png"/>',
        "Chuva moderada": '<img width="110" height="110" src="https://img.icons8.com/ios/100/rain.png"/>',
        "Chuva fraca": '<img width="110" height="110" src="https://img.icons8.com/ios/100/light-rain.png"/>',
        "Tempestade": '<img width="110" height="110" src="https://img.icons8.com/ios/100/storm.png"/>',
        "Neve": '<img width="110" height="110" src="https://img.icons8.com/ios/100/snow.png"/>',
        "Nevoeiro": '<img width="110" height="110" src="https://img.icons8.com/ios/100/fog-day.png"/>',
    }
    icone_noite = '<img width="110" height="110" src="https://img.icons8.com/ios/100/moon-symbol.png"/>'

    if esta_de_noite:
        return icone_noite
    else:
        # Retorna o ícone da condição, ou uma string vazia se a condição não for encontrada
        return icones.get(condicao, "")


# Esta função já estava correta
def get_pizza_chart_html(dispositivos_estado):
    consumo_por_aparelho_ligado = {}
    if not dispositivos_estado:
        return "<p>Carregando estado dos dispositivos...</p>"

    for comodo, dispositivos in dispositivos_estado.items():
        for aparelho, ligado in dispositivos.items():
            if ligado:
                consumo = APARELHOS.get(comodo, {}).get(aparelho, 0)
                nome_limpo = aparelho.replace('_', ' ').title()
                consumo_por_aparelho_ligado[nome_limpo] = consumo

    if not consumo_por_aparelho_ligado:
        return "<p style='text-align:center;'>Nenhum aparelho ligado para exibir no gráfico.</p>"

    data = pd.DataFrame(list(consumo_por_aparelho_ligado.items()), columns=['Categoria', 'Consumo'])
    data = data.sort_values(by='Consumo', ascending=False).head(5)
    fig = px.pie(data, names='Categoria', values='Consumo')
    fig.update_traces(hole=.4)
    fig.update_layout(height=350, width=350, margin=dict(t=0, b=0, l=0, r=0))

    return fig.to_html(full_html=False, include_plotlyjs='cdn')


# CORREÇÃO 3: Implementação completa da função visual da bateria
def get_bateria_visual_html(nivel):
    porcentagem_bateria = (nivel / CAPACIDADE_BATERIA) * 100
    porcentagem_bateria = max(0, min(porcentagem_bateria, 100))
    cor = "#4CAF50" if porcentagem_bateria > 50 else "#FFC107" if porcentagem_bateria > 20 else "#F44336"

    # O CSS para as classes 'bateria-container', 'bateria', 'nivel', etc. já está no style.css
    return f"""
    <div class="bateria-container">
        <div>
            <div class="bateria">
                <div class="nivel" style="width: {porcentagem_bateria}%; background-color: {cor};"></div>
            </div>
            <div class="texto-bateria">{porcentagem_bateria:0.2f}%</div>
            <div class="texto-bateria">Nivel atual: {nivel:0.0f}Wh</div>
            <div class="texto-bateria">Capacidade total: {CAPACIDADE_BATERIA:0.0f}Wh</div>
        </div>
    </div>
    """


# --- Rota Principal ---
@inicio_bp.route('/')
def index():
    try:
        token = get_sems_token()
        status = get_battery_status(token)
        if status is None:
            return "Erro: Não foi possível obter dados da API SEMS.", 500

        nivel_bateria_real = status["soc"] / 100 * CAPACIDADE_BATERIA
        dados = simular("sala", "nenhum", "bateria", nivel_bateria_real)
        if dados is None:
            return "Erro: Não foi possível obter dados de clima.", 500

    except Exception as e:
        return f"Ocorreu um erro ao carregar os dados: {e}", 500

    dispositivos_ativos = []
    sugestao = gerar_sugestao(dados, dispositivos_ativos)

    # Esta linha agora funciona por causa da importação do 'session'
    pizza_chart_html = get_pizza_chart_html(session.get("dispositivos_estado", {}))

    bateria_html = get_bateria_visual_html(nivel_bateria_real)
    clima_icon_html = get_clima_icon_html(dados['condicao_clima'])

    return render_template('inicio.html',
                           active_page='inicio',
                           dados=dados,
                           sugestao=sugestao,
                           pizza_chart_html=pizza_chart_html,
                           bateria_html=bateria_html,
                           clima_icon=clima_icon_html,
                           current_time=datetime.now().strftime("%H:%M"),
                           aviso_noite="- Noite" if datetime.now().hour < 6 or datetime.now().hour > 18 else "")