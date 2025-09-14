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
                <div class="mt-3">Geração atual esperada: {geracao}W</div>
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
                            <h2 class="ms-4 fs-3">Nivel da Bateria</h2>    
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        bateria_visual(novo_nivel)

def container2():
    col1, col2= st.columns(2)
    with col1:
        st.markdown("""
            <div class="chart-container justify-content-start  mt-5">
                    <div class="chart-text">
                        <h2 class="ms-4 fs-3">Sugestão para consumo</h2>    
                    </div>
                </div>
        """, unsafe_allow_html=True)














