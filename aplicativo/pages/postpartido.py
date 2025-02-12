import streamlit as st
import funciones_data as fd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, ColumnsAutoSizeMode, AgGridTheme
import pandas as pd
from mplsoccer import Pitch, VerticalPitch
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import numpy as np
from mplsoccer import Pitch, VerticalPitch, FontManager, Sbopen
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as path_effects
import matplotlib.patches as patches
import funciones_graficas as fg

st.set_page_config(page_title="Tac-Tiq Lab", page_icon='icono.webp',layout="wide",initial_sidebar_state='collapsed')
fg.ajuste_margenes()
fg.diseno_boton()

@st.cache_data()
def leer_partidos():
    partidos = fd.leer_partidos()
    return partidos

partidos = leer_partidos()


if "equipo" in st.session_state and "equipo_imagen" in st.session_state:
    partidos = partidos[(partidos['home_team']==st.session_state['equipo']) | (partidos['away_team']==st.session_state['equipo'])]
    partidos = partidos.sort_values(by=['match_date'])
    tabla_partidos = partidos[['match_date','match_week','home_team','away_team','match_id','home_score','away_score']]
    tabla_partidos.rename(columns={'match_date':'fecha_partido',
                               'match_week':'jornada',
                               'home_team':'equipo_local',
                               'away_team':'equipo_visitante'},inplace=True)
    with st.container():
        col1, col2, col5 = st.columns([1.5,6.5,1.5])
        # Mostrar el logo del equipo
        with col1:
            
            logo_image = "Tac-Tiq_Lab_Logo.png"
            st.image(logo_image, width=200)

        
        if 'partido_seleccionado' in st.session_state:
        
            with col5:
                cambiar = st.button('Cambiar de partido')
    
    col10, col20, col30 = st.columns([1.37,1,1])
    
    if 'partido_seleccionado' not in st.session_state:
        with col10:
            st.write('Seleccione un partido')
            gb = GridOptionsBuilder.from_dataframe(tabla_partidos,editable=False)
            gb.configure_selection(selection_mode="single", use_checkbox=True)
            gb.configure_column('match_id',hide=True)
            gb.configure_column('home_score',hide=True)
            gb.configure_column('away_score',hide=True)
            return_value = AgGrid(tabla_partidos, 
                            gridOptions=gb.build(),
                            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
                            theme=AgGridTheme.STREAMLIT,
                            updateMode=GridUpdateMode.VALUE_CHANGED,
                            allow_unsafe_jscode=True,
                            height=300)
    
        if return_value['selected_rows']:
            st.session_state['partido_seleccionado'] = return_value['selected_rows'][0]
            st.session_state['match_id'] = return_value['selected_rows'][0]['match_id']
            st.rerun()
    if 'partido_seleccionado' in st.session_state:        
        if cambiar:
            del st.session_state['partido_seleccionado']
            st.rerun()

        partido = st.session_state['partido_seleccionado']
        equipo_local = partido['equipo_local']
        equipo_visitante = partido['equipo_visitante']

        with col2:
            fg.mostrar_marcador(partido, equipo_local, equipo_visitante)

        @st.cache_data
        def leer_eventos(match_id):
            eventos =  pd.read_parquet('eventos/eventos_laliga.parquet',filters=[('match_id','==',match_id)])
            
            return eventos
        
        eventos = leer_eventos(st.session_state['match_id'])

        menu1 = option_menu('',options=['Resúmen','Ataque','Defensa'],orientation='horizontal',
                    styles={'container':{'background-color':'#227c9e'},'icon':{'color':'white'},
                                'icon':{'color':'white'},
                                'nav-link':{'color':'white'},
                                'nav-link-selected':{'background-color':'#4f9bb8'}})
        

        if menu1 == 'Resúmen':
            col1, col2, col3, col4, col5 = st.columns([1,0.7,2.3,1,1])
            with col1:
                eventos_iniciales_lst = ['Starting XI','Half Start','Injury Stoppage', 'Player Off', 'Player On', 
                         'Substitution','Half End', 'Tactical Shift', ]
                eventos_iniciales = eventos[eventos['type'].isin(eventos_iniciales_lst)]
                
                formaciones = eventos_iniciales[eventos_iniciales['type']=='Starting XI']
                formaciones.dropna(axis=1,how='all',inplace=True)
                positions, text = fg.grafica_formaciones(formaciones,'Local')
                
            with col2:
                st.write('')
                st.write('')
                st.write('')
                df_positions = pd.DataFrame({"player_id": text, "position_id": positions})
                jugadores = fd.leer_jugdores(text)
                jugadores["nickname_final"] = jugadores.apply(lambda row: row["player_nickname"] if pd.notna(row["player_nickname"]) else row["player_name"], axis=1)
                jugadores = jugadores.merge(df_positions, on="player_id", how="left")
                jugadores = jugadores.sort_values(by="position_id")
                lista_nicks = jugadores["nickname_final"].tolist()

                st.markdown("\n".join(f"- {item}" for item in lista_nicks)) 


            with col4:
                positions, text = fg.grafica_formaciones(formaciones, 'Visitante')
            with col5:
                st.write('')
                st.write('')
                st.write('')
                df_positions = pd.DataFrame({"player_id": text, "position_id": positions})
                jugadores = fd.leer_jugdores(text)
                jugadores["nickname_final"] = jugadores.apply(lambda row: row["player_nickname"] if pd.notna(row["player_nickname"]) else row["player_name"], axis=1)
                jugadores = jugadores.merge(df_positions, on="player_id", how="left")
                jugadores = jugadores.sort_values(by="position_id")
                lista_nicks = jugadores["nickname_final"].tolist()

                st.markdown("\n".join(f"- {item}" for item in lista_nicks)) 

            with col3:
                # Datos de ejemplo (modifica según los reales)
                posesion_equipo_local, posesion_equipo_visitante = fg.calcular_posesion(eventos, equipo_local, equipo_visitante)
                goles_esperados_local, goles_esperados_visitante = fg.goles_esperados(eventos, equipo_local, equipo_visitante)
                total_remates_local, total_remates_visitante = fg.total_remates(eventos,equipo_local,equipo_visitante)
                remates_arco_local, remates_arco_visitante = fg.remates_al_arco(eventos, equipo_local, equipo_visitante)
                corners_local, corners_visitante = fg.tiros_esquina(eventos, equipo_local, equipo_visitante)
                offsides_local, offsides_visitante = fg.offsides(eventos, equipo_local, equipo_visitante)
                pases_completados_local, pct_completados_local, pases_completados_visitante, pct_completados_visitante = fg.pases_completados(eventos, equipo_local, equipo_visitante)

                equipo_local_stats = {
                    "Posesión": posesion_equipo_local,
                    "Goles esperados": goles_esperados_local,
                    "Total Remates": total_remates_local,
                    "Remates al arco": remates_arco_local,
                    "Saques de Esquina": corners_local,
                    "Fueras de Juego": offsides_local,
                    "Pases completados": pases_completados_local,
                    "Efectividad Pases": pct_completados_local
                }

                equipo_visitante_stats = {
                    "Posesión": posesion_equipo_visitante,
                    "Goles esperados": goles_esperados_visitante,
                    "Total Remates": total_remates_visitante,
                    "Remates al arco": remates_arco_visitante,
                    "Saques de Esquina": corners_visitante,
                    "Fueras de Juego": offsides_visitante,
                    "Pases completados": pases_completados_visitante,
                    "Efectividad Pases": pct_completados_visitante
                }

                # Estilo de fondo
                st.markdown(
                    """
                    <style>
                        
                        .row {
                            display: flex;
                            align-items: center;
                            justify-content: space-between;
                            padding: 10px 0;
                            border-bottom: 1px solid #333;
                            text-align: center;
                        }
                        .stat-left, .stat-right {
                            font-size: 16px;
                            font-weight: bold;
                            width: 20%;
                            text-align: center;
                        }
                        .stat-name {
                            font-size: 16px;
                            font-weight: bold;
                            flex-grow: 1;
                            text-align: center;
                        }
                        
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                # Renderizar estadísticas en filas (sin la franja superior)
                st.markdown('<div class="container">', unsafe_allow_html=True)

                for stat in equipo_local_stats.keys():
                    st.markdown(
                        f"""
                        <div class="row">
                            <div class="stat-left">
                                <div class="stat-circle">{equipo_local_stats[stat]}</div>
                            </div>
                            <div class="stat-name">{stat}</div>
                            <div class="stat-right">{equipo_visitante_stats[stat]}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown("</div>", unsafe_allow_html=True)

        elif menu1 == 'Ataque':
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([1,0.7,2.3,1,1]) 
                with col1:
                    eventos_ataque_lst = ['Pass','Ball Receipt*','Carry','Miscontrol','Dribble','Duel','Shot','Foul Won']
                    eventos_ataque = eventos[eventos['type'].isin(eventos_ataque_lst)]
                    eventos_ataque[['x', 'y']] = pd.DataFrame(eventos_ataque['location'].tolist(), index=eventos_ataque.index)
                    event = st.selectbox('Evento',options=sorted(eventos_ataque_lst))
                with col2:
                    st.metric('erejo',2348)
            
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([1,0.7,2.3,1,1]) 
                evento_local = eventos_ataque[(eventos_ataque['type']==event)&(eventos_ataque['team']==equipo_local)]
                evento_visitante = eventos_ataque[(eventos_ataque['type']==event)&(eventos_ataque['team']==equipo_visitante)]
                with col1:
                    fg.generar_mapa_calor(evento_local)

                with col4:
                    fg.generar_mapa_calor(evento_visitante)

                

        elif menu1 == 'Defensa':
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([1,0.7,2.3,1,1]) 
                with col1:
                    eventos_defensa_lst = ['Pressure','Duel','Interception','Goal Keeper','Clearance','Ball Recovery',
                       'Foul Committed','Dribbled Past','Block']
                    eventos_defensa = eventos[eventos['type'].isin(eventos_defensa_lst)]
                    eventos_defensa[['x', 'y']] = pd.DataFrame(eventos_defensa['location'].tolist(), index=eventos_defensa.index)
                    event = st.selectbox('Evento',options=sorted(eventos_defensa_lst))
                with col2:
                    st.metric('erejo',2348)
            
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([1,0.7,2.3,1,1]) 
                evento_local = eventos_defensa[(eventos_defensa['type']==event)&(eventos_defensa['team']==equipo_local)]
                evento_visitante = eventos_defensa[(eventos_defensa['type']==event)&(eventos_defensa['team']==equipo_visitante)]
                with col1:
                    fg.generar_mapa_calor(evento_local)

                with col4:
                    fg.generar_mapa_calor(evento_visitante)
            

else:
    st.switch_page('inicio.py')