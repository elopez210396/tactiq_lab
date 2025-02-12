import streamlit as st

st.set_page_config(page_title="Tac-Tiq Lab", page_icon='icono.webp',layout="wide",initial_sidebar_state='collapsed')
logo_image = "Tac-Tiq_Lab_Logo.png"
st.image(logo_image, width=200)
st.markdown("""
    <style>
    .stButton:nth-child(1) button {
        background-color: #227c9e;  /* Color para el primer botón */
        color: white;
        border-radius: 8px;
        padding: 80px 20px;
        font-size: 20px;
        font-weight: bold;
        width: 80%;
    }
    </style>
    """, unsafe_allow_html=True)

st.title('')

if 'equipo_objetivo' in st.session_state:    
    col1, col2 = st.columns([1, 1])
    with col1:
        pre_partido = st.button("Pre-partido")
        if pre_partido:
            st.session_state['analisis_objetivo'] = 'pre_partido'
            st.switch_page('pages/prepartido.py')
    with col2:
        post_partido = st.button("Post-partido")
        if post_partido:
            st.session_state['analisis_objetivo'] = "post_partido"
            st.switch_page('pages/postpartido.py')
else:
    st.switch_page('inicio.py')