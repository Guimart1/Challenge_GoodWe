import streamlit as st
import os
import requests
from backend.config import APARELHOS, CONSUMO_STANDBY, CAPACIDADE_BATERIA
from backend.assistente_energia import gerar_sugestao_comodo
from backend.simulador import simular
from backend.conexao_sems import crosslogin, get_inverter_list_demo, get_full_battery_status
from backend.estado_dispositivos import toggle_dispositivo, get_dispositivos_ativos
import base64


def container_gerenciamento():
    if "dispositivos_estado" not in st.session_state:
        st.session_state["dispositivos_estado"] = {
            comodo: {chave: False for chave in APARELHOS.get(comodo, {})}
            for comodo in APARELHOS
        }
    # --- CONFIGURAÇÃO DA PÁGINA ---
    st.set_page_config(
        page_title="Dashboard de Energia",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # --- FUNÇÃO PARA CARREGAR ÍCONES COMO BASE64 ---
    # Isso garante que os ícones sempre carreguem e evita dependências de links externos
    def get_image_as_base64(path):
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    # --- ÍCONES  ---
    icon_sofa = "https://cdn-icons-png.flaticon.com/512/1010/1010398.png"
    icon_kitchen = "https://cdn-icons-png.flaticon.com/512/3565/3565450.png"
    icon_bed = "https://static.vecteezy.com/system/resources/previews/003/685/225/non_2x/a-bed-icon-illustration-vector.jpg"
    icon_shower = "https://img.freepik.com/vetores-premium/vetor-do-icone-do-chuveiro-isolado-no-fundo-branco_824631-260.jpg?semt=ais_hybrid&w=740&q=80"
    icon_car = "https://img.freepik.com/premium-vector/car-icon-vehicle-icon-car-vector-icon_564974-1452.jpg?w=360"
    icon_plus = "https://static.thenounproject.com/png/2310577-200.png"
    icon_lightning = "https://static.thenounproject.com/png/2039810-200.png"
    icon_home = "https://img.freepik.com/premium-vector/minimal-house-icon-website-symbol-vector-site-sign-ui-home-icon-home-creative-icon-minimalis_619470-390.jpg"

    # --- ESTILOS CSS ---
    st.markdown("""
        <style>
            /* Remove o padding padrão do Streamlit para o corpo */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                padding-left: 3rem;
                padding-right: 3rem;
            }
            /* Define a cor de fundo da página */
            body {
                background-color: #f0f2f6;
            }

            /* --- Estilos do Header (Navbar) --- */
            .navbar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px;
                background-color: #FFFFFF;
                border-radius: 50px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                width: 100%;
                margin-bottom: 30px;
            }
            .nav-icons {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            .icon-circle {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                border: 3px solid #022840;
                display: flex;
                justify-content: center;
                align-items: center;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .icon-circle img {
                width: 32px;
                height: 32px;
            }
            .icon-circle.active {
                background-color: #FFD51C; /* Amarelo */
            }
            .icon-circle:not(.active):hover {
                background-color: #e0e0e0;
            }
            .hamburger, .plus {
                padding: 10px;
            }

            /* --- Estilos dos Títulos de Seção (Amarelos) --- */
            .section-title {
                background: #FFD51C;
                padding: 10px 30px;
                border-radius: 28px;
                font-size: 1.4em;
                font-weight: bold;
                color: black;
                display: inline-block;
                margin-bottom: 15px;
            }

            /* --- Estilos dos Containers de Seção (Cinzas) --- */
            .gray-container {
                background: #e9e9ed;
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }

            /* --- Estilos dos Botões de Eletrônicos --- */
            .device-button {
                display: flex;
                align-items: center;
                background: #022840;
                width: 100%;
                padding: 10px 15px;
                border-radius: 25px;
                color: white;
                text-decoration: none;
                transition: opacity 0.3s;
                margin-bottom: 15px;
            }
            .device-button:hover {
                opacity: 0.8;
                cursor: pointer;
            }
            .device-button .icon-square {
                background: #FFFFFF;
                width: 48px;
                height: 48px;
                border-radius: 10px;
                display: flex;
                justify-content: center;
                align-items: center;
                margin-right: 20px;
            }
            .device-button .icon-square img {
                width: 30px;
                height: 30px;
            }
            .device-button .text {
                font-size: 1.2em;
                font-weight: bold;
            }

            /* --- Estilos da Seção de Redirecionamento --- */
            .redirection-container {
                text-align: center;
            }
            .redirection-container p {
                font-size: 1em;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }
            .residencia-button {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 15px;
                background: #022840;
                width: 100%;
                padding: 18px 15px;
                border-radius: 25px;
                color: white;
                font-size: 1.2em;
                font-weight: bold;
                cursor: pointer;
                transition: opacity 0.3s;
            }
            .residencia-button:hover {
                opacity: 0.8;
            }
            .residencia-button img {
                width: 32px;
                height: 32px;
            }

            /* --- Estilos da Seção de Recomendações --- */
            .recommendations-container {
                min-height: 250px; /* Altura ajustável */
                height:auto;
                display: flex;
                align-items: flex-start;
                padding-left: 25px;
            }
            .recommendations-container p {
                font-size: 1.1em;
                font-weight: bold;
                color: #555;
            }
        </style>
    """, unsafe_allow_html=True)

    # LÓGICA PARA CONTROLAR O ESTADO DA PÁGINA ---
    # Verifica se há um parâmetro 'page' na URL para determinar o que exibir.
    query_params = st.query_params
    page_state = query_params.get("page")

    # --- LAYOUT DA PÁGINA ---

    st.markdown(f"""
        <div class="navbar">
            <div class="nav-icons hamburger">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32"
                     viewBox="0 0 24 24" fill="none" stroke="currentColor"
                     stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                     <line x1="4" x2="20" y1="12" y2="12"/>
                     <line x1="4" x2="20" y1="6" y2="6"/>
                     <line x1="4" x2="20" y1="18" y2="18"/>
                </svg>
            </div>
            <div class="nav-icons">
                <a href="?page=gerenciamento&room=sala" target="_self">
                    <div class="icon-circle"><img src="{icon_sofa}"></div>
                </a>
                <a href="?page=gerenciamento&room=cozinha" target="_self">
                    <div class="icon-circle"><img src="{icon_kitchen}"></div>
                </a>
                <a href="?page=gerenciamento&room=quarto" target="_self">
                    <div class="icon-circle"><img src="{icon_bed}"></div>
                </a>
                <a href="?page=gerenciamento&room=banheiro" target="_self">
                    <div class="icon-circle"><img src="{icon_shower}"></div>
                </a>
                <a href="?page=gerenciamento&room=garagem" target="_self">
                    <div class="icon-circle"><img src="{icon_car}"></div>
                </a>
            </div>
            <div class="nav-icons plus">
                <div class="icon-circle"><img src="{icon_plus}"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Corpo principal
    col1, col2 = st.columns([2, 1])

    with col1:
        page = st.query_params.get("page", "gerenciamento").lower()

        if page == "gerenciamento":
            comodo = st.query_params.get("room", "sala").lower()
            dispositivos = APARELHOS.get(comodo, {})

            st.markdown(f"<div class='section-title'>ELETRÔNICOS ATIVOS — {comodo.upper()}</div>",
                        unsafe_allow_html=True)
            consumo_total = CONSUMO_STANDBY

            for chave, consumo in dispositivos.items():
                ligado = toggle_dispositivo(comodo, chave)

                cor = "#4CAF50" if ligado else "#F44336"
                estado = "Ligado" if ligado else "Desligado"
                nome_formatado = chave.replace("_", " ").upper()

                if ligado:
                    consumo_total += consumo

                st.markdown(f"""
                    <div class="device-button">
                        <div class="icon-square"><img src="{icon_lightning}"></div>
                        <div class="text">{nome_formatado} - 
                        <span style='color:{cor}; font-weight:bold;'>{estado}</span></div>
                    </div>
                """, unsafe_allow_html=True)
            # Gera sugestão com base nos dados reais
            try:
                token = crosslogin(os.getenv("SEMS_ACCOUNT", "demo@goodwe.com"),
                                   os.getenv("SEMS_PASSWORD", "GoodweSems123!@#"))
                inverters = get_inverter_list_demo(token)
                inverter_id = inverters["data"][0]["id"]
                status_bateria = get_full_battery_status(token, inverter_id)
                soc_bateria = status_bateria.get("soc", 0)
                nivel_bateria_real = CAPACIDADE_BATERIA * (soc_bateria / 100)

                dados = simular(comodo, "", "", nivel_bateria_real)
                dispositivos_ativos = get_dispositivos_ativos(comodo)
                sugestao_comodo = gerar_sugestao_comodo(comodo, dispositivos_ativos, dados)

            except (requests.exceptions.RequestException, RuntimeError) as e:
                sugestao_comodo = f"Não foi possível obter dados da bateria. Erro: {e}"

            st.markdown('<div class="section-title">RECOMENDAÇÕES</div>', unsafe_allow_html=True)
            st.markdown(f"""
                <div class="gray-container recommendations-container">
                    <p>{sugestao_comodo}</p>
                </div>
            """, unsafe_allow_html=True)
    with col2:
        # 2.3. Seção de Redirecionamento
        st.markdown('<div class="section-title">REDIRECIONAMENTO</div>', unsafe_allow_html=True)

        # RENDERIZAÇÃO CONDICIONAL ---
        # Se a URL contiver 'page=kitchen', exibe o container em branco. Caso contrário, exibe o conteúdo padrão.
        if page_state == "kitchen":
            redirecionamento_html = """
                <div class="gray-container redirection-container" style="height: 142px; display: flex; align-items: center; justify-content: center;">
                     <p style='color: #888; font-weight: bold;'>Nenhuma ação de redirecionamento disponível.</p>
                </div>
            """
        else:
            redirecionamento_html = f"""
                <div class="gray-container redirection-container">
                    <p>DIRECIONAR A ENERGIA GERADA PARA:</p>
                    <div class="residencia-button">
                        <img src="{icon_home}">
                        <span>RESIDÊNCIA</span>
                    </div>
                </div>
            """
        st.markdown(redirecionamento_html, unsafe_allow_html=True)
        # --- FIM DA MODIFICAÇÃO 4 ---


# Chamar a função para executar a aplicação
if __name__ == "__main__":
    container_gerenciamento()