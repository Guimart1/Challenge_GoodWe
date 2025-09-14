import streamlit as st


def sidebar(pagina):
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
        [data-testid="stSidebarContent"]{
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
            height: 15%;
            align-items: end;
            justify-content: center;
            border-top: 1px solid #D9D9D9;
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
        a {
            text-decoration: none !important;
            color: #fff !important;
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
            transition: 0.5s;
        }
        .side-element:hover {
            background-color: #025373 !important;
            transition: 0.5s ease;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(f"""
        <div class="titulo">QiSun</div>
        <div class="side-container">
            <div class="side-list">
                <a href="/?page=Ínicio" target="_self">
                    <div class="side-element" style="background-color: {'#025373' if pagina == 'Ínicio' else 'inherit'}">Ínicio</div>
                </a>
                <a href="/?page=Bateria" target="_self">
                    <div class="side-element" style="background-color: {'#025373' if pagina == 'Bateria' else 'inherit'}">Bateria</div>
                </a>
                <a href="/?page=Gerenciamento" target="_self">
                    <div class="side-element" style="background-color: {'#025373' if pagina == 'Gerenciamento' else 'inherit'}">Gerenciamento</div>
                </a>
                <a href="/?page=Painel Solar" target="_self">
                    <div class="side-element" style="background-color: {'#025373' if pagina == 'Painel Solar' else 'inherit'}">Painel Solar</div>
                </a>
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
