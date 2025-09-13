import pandas as pd
from datetime import datetime
import streamlit as st
import plotly.express as px
from config import categorias, valores
import time
from streamlit_autorefresh import st_autorefresh

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
            height: 92vh;
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

        """,unsafe_allow_html=True)



def container1():

    st.markdown("""
    <style>
        @font-face {
            font-family: 'Digital';
            src: url('/static/fonts/DS-DIGI.TTF') format('truetype');
        }
        .text-clock {
            font-family: 'Digital', sans-serif;
            font-size: 2em;
            color: #fff;
        }
    </style>
    
    """, unsafe_allow_html=True)

    data = pd.DataFrame({'Categoria': categorias, 'Valor': valores})
    fig = px.pie(data, names='Categoria', values='Valor', title='Consumo por Aparelho')

    col1, col2, col3 = st.columns(3)
    with col1:
        current_time = datetime.now().strftime("%H:%M")
        st.markdown(f"<h2 class='text-clock'>{current_time}</h2>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="element"></div>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
    with col3:
        st.markdown('<div class="element-container">teste</div>', unsafe_allow_html=True)







