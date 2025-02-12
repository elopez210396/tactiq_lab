import streamlit as st
import os

# Configuración inicial
st.set_page_config(page_title="Tac-Tiq Lab", page_icon='icono.webp',layout="wide",initial_sidebar_state='collapsed')
logo_image = "Tac-Tiq_Lab_Logo.png"
st.image(logo_image, width=200)

if 'equipo' in st.session_state:
    del st.session_state['equipo']
# Ruta de la carpeta con los escudos
escudos_folder = "logos_laliga"

# Generar diccionario de equipos automáticamente
equipos_imagenes = {
    os.path.splitext(imagen)[0].replace("_", " ").title(): imagen
    for imagen in os.listdir(escudos_folder)
    if imagen.endswith(".png")
}

# Lista oficial de equipos
equipos_oficiales = ['Athletic Club',
 'Atlético Madrid',
 'Barcelona',
 'Betis',
 'Celta Vigo',
 'Eibar',
 'Espanyol',
 'Getafe',
 'Granada',
 'La Coruña',
 'Las Palmas',
 'Levante',
 'Málaga',
 'Rayo Vallecano',
 'Real Madrid',
 'Real Sociedad',
 'Sevilla',
 'Sporting Gijón',
 'Valencia',
 'Villarreal']

# Normalización de nombres (para hacer match)
def normalizar_nombre(nombre):
    return nombre.lower().replace(" ", "").replace("_", "")

# Muestra de los escudos
st.title("Seleccione un equipo")
columns = st.columns(10)  # Muestra 10 escudos por fila

for i, (equipo, imagen) in enumerate(equipos_imagenes.items()):
    col = columns[i % 10]  # Cambia de columna cada 10 equipos
    with col:
        if st.button(label=equipo, use_container_width=True):  # Botón con el nombre del equipo
            # Guardar en `st.session_state`
            equipo_seleccionado = next(
                (oficial for oficial in equipos_oficiales if normalizar_nombre(oficial) == normalizar_nombre(equipo)),
                equipo  # Fallback por si no hay match exacto
            )
            
            st.session_state["equipo"] = equipo_seleccionado
            st.session_state["equipo_imagen"] = imagen

        # Muestra el escudo
        st.image(os.path.join(escudos_folder, imagen), use_column_width=True)
        hide_img_fs = '''
        <style>
        button[title="View fullscreen"]{
            visibility: hidden;}
        </style>
        '''

        st.markdown(hide_img_fs, unsafe_allow_html=True)
if "equipo" in st.session_state:
    st.switch_page("pages/inicio2.py")
