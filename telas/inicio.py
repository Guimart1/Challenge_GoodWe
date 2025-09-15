import pandas as pd
import plotly.express as px
from backend.simulador import *
from backend.assistente_energia import *
from backend.conexao_sems import *
from backend.config import *
import base64


def local_font_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

 # ALTERAR ICONE DE ACORDO COM ESTADO DO CLIMA:
def clima_icon(condicao):
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
        return icones.get(condicao, "")


def pizza_chart():
    consumo_por_aparelho = {}

    for comodo, dispositivos in APARELHOS.items():
        for aparelho, consumo in dispositivos.items():
            # Usa apenas o nome do aparelho para o gráfico
            nome_limpo = aparelho.replace('_', ' ').title()

            # Soma o consumo caso o mesmo aparelho apareça em cômodos diferentes
            consumo_por_aparelho[nome_limpo] = consumo_por_aparelho.get(nome_limpo, 0) + consumo

    if not consumo_por_aparelho:
        st.info("Nenhum aparelho encontrado para exibir no gráfico.")
        return

    # Converte o dicionário para um DataFrame, ordena e pega os 5 maiores
    data = pd.DataFrame(list(consumo_por_aparelho.items()), columns=['Categoria', 'Consumo'])
    data = data.sort_values(by='Consumo', ascending=False).head(5)

    fig = px.pie(data, names='Categoria', values='Consumo')
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=14, color="black")
        )
    )

    return st.plotly_chart(fig, use_container_width=True)


def bateria_visual(nivel):
    porcentagem_bateria = (nivel / CAPACIDADE_BATERIA) * 100
    porcentagem_bateria = max(0, min(porcentagem_bateria, 100))
    cor = "#4CAF50" if porcentagem_bateria > 50 else "#FFC107" if porcentagem_bateria > 20 else "#F44336"

    st.markdown(f"""
    <style>
        [data-testid="stMainBlockContainer"]{{
            padding-top: 5%;
        }}
        .bateria-container{{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 400px;
        }}
        .bateria {{
            width: 200px;
            height: 100px;
            border: 5px solid #333;
            border-radius: 10px;
            position: relative;
            background-color: #ddd;
            margin: auto;
        }}
        .bateria::after {{
            content: "";
            position: absolute;
            top: 35%;
            right: -30px;
            width: 5px;
            height: 30px;
            background: #333;
            border-radius: 3px;
        }}
        .nivel {{
            height: 100%;
            width: {porcentagem_bateria}%;
            background-color: {cor};
            border-radius: 5px;
            transition: 1s;
        }}
        .texto-bateria {{
            text-align: center;
            font-weight: bold;
            margin-top: 10px;
        }}
    </style>
    <div class="bateria-container">
        <div class="bateria">
            <div class="nivel"></div>
            <div class="texto-bateria">{porcentagem_bateria:02.2f}%</div>
            <div class="texto-bateria">Nivel atual: {nivel:0.0f}Wh</div>
            <div class="texto-bateria">Capacidade total: {CAPACIDADE_BATERIA:0.0f}Wh</div>
        </div>
    </div>

    """, unsafe_allow_html=True)


def container_dash(dados, status): # CONTAINER DE INFOS PRINCIPAIS
    font_base64 = local_font_to_base64("./static/fonts/DS-DIGIB.TTF")
    st.markdown(f"""
    <style>
        @font-face {{
            font-family: "Digital";
            src: url(data:font/ttf;base64,{font_base64}) format('truetype');
        }}
        .text-clock {{
            font-family: "Digital", sans-serif !important;
            font-size: 5em !important;
            color: #000 !important;
            font-weight: bold;
        }}
        .container-icon {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100%;
            font-weight: bold;
        }}
        .chart-container {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .chart-text {{
            width: 70%;
            text-align: center !important; 
            background-color: #F0CA1F ;
            border-radius: 50px;
            font-weight: bold;
            height: 80%;
        }}
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)


    def aviso_noite():
        hora_atual = datetime.now().hour
        if hora_atual < 6 or hora_atual > 18:
            return "- Noite"
        else:
            return ""

    with col1:
        current_time = datetime.now().strftime("%H:%M")
        st.markdown(f"""
            <div class="container-icon">
                <h2 class="text-clock mt-5">{current_time}</h2>
                <div class="mt-3">{clima_icon(dados['condicao_clima'])}</div>
                <div class="mt-2 fs-5">{dados['condicao_clima']} | {dados['temperatura']}°C</div>
                <div class="mt-3">Geração atual esperada: {dados['geracao_solar']}W {aviso_noite()}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="chart-container">
                <div class="chart-text">
                    <h2 class="ms-4 fs-4">CONSUMO DE ENERGIA</h2>    
                </div>
            </div>
        """, unsafe_allow_html=True)

        pizza_chart()

    nivel_bateria = status["soc"] / 100 * CAPACIDADE_BATERIA  # Convertendo % para Wh
    with col3:
        st.markdown(f"""
                    <div class="chart-container">
                        <div class="chart-text">
                            <h2 class="ms-4 fs-4">NIVEL DA BATERIA</h2>    
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        bateria_visual(nivel_bateria)


def container_text_ia():
    col1, col2 = st.columns(2)
    st.markdown("""
        <style>
            .ai-container {
                background: #e9e9ed;
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            .ai-text {
                font-weight: 600;
                color: #555555 !important;
            }
            .consumo-click {
                cursor: pointer;
                color: #000 !important;
                text-decoration: none;
            }
        </style>
        """, unsafe_allow_html=True)

    with col1:
        st.markdown("""
            <div class="chart-container justify-content-start">
                <div class="chart-text sugestao">
                    <h2 class="ms-4 fs-4">SUGESTÃO PARA CONSUMO</h2>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Exibe sugestão se já estiver gerada
        if "sugestao" in st.session_state:
            st.markdown(f"""
                <div class="ai-container mt-5">
                    <p class="ai-text">{st.session_state.sugestao}</p>
                </div>
            """, unsafe_allow_html=True)


def container_inicio():
    acc = "demo@goodwe.com"
    pwd = "GoodweSems123!@#"
    token = crosslogin(acc, pwd, region="us")
    inverters = get_inverter_list_demo(token, region="eu")
    inverter_id = inverters["data"][0]["id"]

    if "status_bateria" not in st.session_state:
        st.session_state.status_bateria = get_full_battery_status(token, inverter_id)

    status = st.session_state.status_bateria
    nivel_bateria_real = status["soc"] / 100 * CAPACIDADE_BATERIA

    comodo = st.query_params.get("page", "sala").lower()

    aparelhos_lista = list(APARELHOS.get(comodo, {}).keys())
    aparelho_default = aparelhos_lista[0] if aparelhos_lista else "nenhum"

    st.session_state.select_aparelho_hidden = aparelho_default
    st.session_state.radio_redirecionamento_hidden = "bateria"

    aparelho = st.session_state.select_aparelho_hidden
    redirecionamento = st.session_state.radio_redirecionamento_hidden

    dados, sugestao_padrao = gerar_sugestao(comodo, aparelho, redirecionamento, nivel_bateria_real)
    st.session_state.dados = dados

    container_dash(dados, status)

    st.session_state.sugestao = sugestao_padrao

    container_text_ia()











