import pandas as pd
from datetime import datetime
import streamlit as st
import plotly.express as px
from config import categorias, valores, NIVEL_INICIAL_BATERIA, CAPACIDADE_BATERIA, CONSUMO_STANDBY, APARELHOS
from backend import obter_dados_clima, calcular_geracao_solar

import base64

def local_font_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def sidebar():
    scripts = """
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    """
    st.markdown(scripts, unsafe_allow_html=True)
    st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&display=swap" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@160..700&display=swap" rel="stylesheet">
    <style>
        [data-testid="stSidebar"] {
            background-color: #022840; 
            color: white;
            opacity: 100%;
        }
        [data-testid="stSidebarUserContent"]{
            padding: 0;
        }
        .titulo {
            font-size: 2em;
            color: #f5a623;
            text-align: center;
            font-family: 'lexend';
            margin-bottom: 20px
        }

        .side-list {
            height: 50%;
            width: 100%;
        }

        .user-container{
            display: flex;
            width: 100%;
            height: 30%;
            align-items: end;
            justify-content: center;
        }

        .user-box{
            display: flex;
            align-items: center;
            justify-content: start;
            height: 50px;
            width: 95%;
            background-color: #D9D9D9;
            border-radius: 35px;
        }

        .side-container{
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 80vh;
            width: 100%;
            font-family: Readex Pro;
        }
        .side-element {
            display: flex;
            background-color: inherit;
            height: 50px;
            cursor: pointer;
            align-items: center;
            padding-left: 10px;
            border-radius: 10px;
            font-size: 1.3em;
        }
        .side-element:hover {
            background-color: #025373
        }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("""
        <div class="titulo">QiSun</div>
        <div class="side-container">
            <div class="side-list">
                <div class="side-element">Ínicio</div>
                <div class="side-element">Bateria</div>
                <div class="side-element">Gerenciamento</div>
                <div class="side-element">Painel Solar</div>
            </div>
            <div class="user-container">
                <div class="user-box">
                    <div style="width: 50px; display: flex; justify-content: center;">
                        <img width="30" height="30" src="https://img.icons8.com/ios-glyphs/30/user--v1.png" alt="user--v1"/>                    
                    </div>
                    <div style="color: #000000;">                    
                        <p style="margin: 0; font-size: 1em;">Nome Usuário</p>
                        <p style="margin: 0; font-size: 0.8em;">Info Usuário</p>   
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def clima_icon(dados): # ALTERAR ICONE DE ACORDO COM ESTADO DO CLIMA:
    condicao = dados["current"]["condition"]["text"]
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
    return icones.get(condicao, "")

def pizza_chart(): # GRAFICO DE PIZZA POR CONSUMO
    data = pd.DataFrame({'Categoria': categorias, 'Consumo': valores})
    fig = px.pie(data, names='Categoria', values='Consumo')
    fig.update_layout(
        legend=dict(
            orientation="h",  # horizontal
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=14, color="black")
        )
    )

    return  st.plotly_chart(fig, use_container_width=True)


def bateria_visual(nivel):
    porcentagem_bateria = (nivel / CAPACIDADE_BATERIA) * 100
    porcentagem_bateria = max(0, min(porcentagem_bateria, 100))
    cor = "#4CAF50" if porcentagem_bateria > 50 else "#FFC107" if porcentagem_bateria > 20 else "#F44336"

    st.markdown(f"""
    <style>
        [data-testid="stMainBlockContainer"]{{
            padding-top: 0;
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
        </div>
    </div>

    """, unsafe_allow_html=True)

def container1(): # CONTAINER DE INFOS PRINCIPAIS
    font_base64 = local_font_to_base64("static/fonts/DS-DIGIB.TTF")
    dados = obter_dados_clima()
    if not dados:
        st.error("Erro ao obter dados de clima.")
        st.stop()

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
        }}
        .chart-container {{
            display: flex;
            justify-content: center;
        }}
        .chart-text {{
            width: 70%;
            text-align: center !important; 
            background-color: #F0CA1F ;
            border-radius: 50px;
            font-weight: bold;
        }}
    </style>
    """, unsafe_allow_html=True)

    nivel_bateria = NIVEL_INICIAL_BATERIA

    geracao = calcular_geracao_solar(dados)
    col1, col2, col3 = st.columns(3)

    geracao = calcular_geracao_solar(dados)

    aparelho = st.selectbox("Escolha um aparelho:", ["nenhum"] + list(APARELHOS.keys()))
    consumo = APARELHOS.get(aparelho, 0) + CONSUMO_STANDBY
    redirecionamento = st.radio("Redirecionar energia para:", ["bateria", "casa"])

    if redirecionamento == "bateria":
        energia_para_bateria = max(0, geracao - consumo)
        novo_nivel = min(nivel_bateria + energia_para_bateria, CAPACIDADE_BATERIA)
        st.success(f"🔋 Energia para bateria: {energia_para_bateria} W | Nível final: {novo_nivel} Wh")
    else:
        energia_necessaria = max(0, consumo - geracao)
        if nivel_bateria >= energia_necessaria:
            novo_nivel = nivel_bateria - energia_necessaria
            st.success(f"🏠 Energia da bateria usada: {energia_necessaria} W | Nível final: {novo_nivel} Wh")
        else:
            novo_nivel = nivel_bateria
            st.warning("⚠️ Bateria insuficiente. Usando rede elétrica.")

    with col1:
        current_time = datetime.now().strftime("%H:%M")
        st.markdown(f"""
            <div class="container-icon">
                <h2 class="text-clock mt-5">{current_time}</h2>
                <div class="mt-3">{clima_icon(dados)}</div>
                <div class="mt-2 fs-5">{dados['current']['condition']['text']} | {dados['current']['temp_c']}°C</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="chart-container">
                <div class="chart-text">
                    <h2 class="ms-4 fs-3">Consumo de Energia</h2>    
                </div>
            </div>
        """, unsafe_allow_html=True)

        pizza_chart()  # Renderiza o gráfico fora do HTML

    with col3:
        st.markdown(f"""
                    <div class="chart-container">
                        <div class="chart-text">
                            <h2 class="ms-4 fs-3">Nivel de Energia</h2>    
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        bateria_visual(novo_nivel)

def container2():
    st.markdown("""
        <div class="chart-container justify-content-start  mt-5">
                <div class="chart-text w-25">
                    <h2 class="ms-4 fs-3">Sugestão para consumo</h2>    
                </div>
            </div>
    """, unsafe_allow_html=True)














