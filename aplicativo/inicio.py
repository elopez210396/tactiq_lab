import streamlit as st

st.set_page_config(page_title="Tac-Tiq Lab", page_icon='icono.webp',layout="wide",initial_sidebar_state='collapsed')
col1, col2, col3 = st.columns([2, 4, 2])
with col2:
    logo_image = "Tac-Tiq_Lab_Logo.png"
    st.image(logo_image, width=700)

st.markdown("""
    <style>
    .stButton:nth-child(1) button {
        background-color: #227c9e;  /* Color para el primer botón */
        color: white;
        border-radius: 8px;
        padding: 40px;
        font-size: 40px !important;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

if 'equipo_objetivo' in st.session_state:
    del st.session_state['equipo_objetivo']

col1, col2, col3, col4 = st.columns([2, 2, 2, 2.3])
with col2:  
    equipo_propio = st.button("Equipo propio")
    if equipo_propio:
        st.session_state['equipo_objetivo'] = "propio"
with col3:
    equipo_rival = st.button("Equipo rival")
    if equipo_rival:
        st.session_state['equipo_objetivo'] = "rival"

if 'equipo_objetivo' in st.session_state:
    if st.session_state['equipo_objetivo'] == 'propio':
        st.session_state['equipo'] = 'Valencia'
        st.session_state['equipo_imagen'] = 'Valencia.png'
        st.switch_page('pages/inicio2.py')
    elif st.session_state['equipo_objetivo'] == 'rival':
        st.switch_page('pages/equipos.py')
     
    