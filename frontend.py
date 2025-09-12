import streamlit as st

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
    <style>
        [data-testid="stSidebar"] {
            background-color: #022840;  /* azul escuro */
            color: white;
        }
    .titulo {
        font-size: 2em;
        color: #f5a623;
        text-align: center;
        font-family: 'lexend';
    }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("""<div class="titulo">QiSun</div>""",unsafe_allow_html=True)








