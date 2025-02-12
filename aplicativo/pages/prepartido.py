import streamlit as st
from streamlit_option_menu import option_menu
import funciones_data as fd

st.set_page_config(page_title="Tac-Tiq Lab", page_icon='icono.webp',layout="wide",initial_sidebar_state='collapsed')

@st.cache_data()
def leer_partidos():
    partidos = fd.leer_partidos()
    return partidos



if "equipo" in st.session_state and "equipo_imagen" in st.session_state:
    partidos = leer_partidos()
    partidos = partidos[(partidos['home_team']==st.session_state['equipo']) | (partidos['away_team']==st.session_state['equipo'])]
    partidos = partidos.sort_values(by=['match_date'])
    
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([1,5,1,1,1.5])

        # Mostrar el logo del equipo
        with col1:
            escudos_folder = "logos_laliga"  # Ajusta la ruta si es necesario
            st.image(f"{escudos_folder}/{st.session_state['equipo_imagen']}", width=80)
            hide_img_fs = '''
            <style>
            button[title="View fullscreen"]{
                visibility: hidden;}
            </style>'''
            
            st.markdown(hide_img_fs, unsafe_allow_html=True)

        with col2:
            menu = option_menu(None, ['General','Equipo','Jugador'], default_index=0, orientation="horizontal",
                            styles={'container':{'background-color':'#245D93'},'icon':{'color':'orange'},
                                'icon':{'color':'orange'},
                                'nav-link':{'color':'orange'},
                                'nav-link-selected':{'background-color':'#0068C9'}})
    if menu != 'General':

        with col4:
            condicion = st.selectbox('Condición', ['Todos', 'Local', 'Visitante'])
        with col5:
            num_partidos = st.selectbox("Partidos",['Últimos 5', 'Últimos 10', 'Todos'])

        if condicion == 'Local':
            partidos = partidos[partidos['home_team'] == st.session_state['equipo']]
        elif condicion == 'Visitante':
            partidos = partidos[partidos['away_team'] == st.session_state['equipo']]  
        partidos = partidos.sort_values(by=['match_date'])
        if num_partidos == 'Últimos 5':
            partidos = partidos.tail(5)
        elif num_partidos == 'Últimos 10':
            partidos = partidos.tail(10)

else:
    st.switch_page('inicio.py')