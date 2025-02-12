import streamlit as st
from mplsoccer import Pitch, VerticalPitch
import numpy as np
from mplsoccer import Pitch, VerticalPitch, FontManager, Sbopen
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as path_effects

def generar_mapa_calor (evento):
    pitch = VerticalPitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#22312b')
    pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",['#227c9e', '#46cd7a'], N=10)
    path_eff = [path_effects.Stroke(linewidth=3, foreground='black'),
                path_effects.Normal()]  
                                                                                                                    
    fig, axs = pitch.grid(endnote_height=0.01, endnote_space=0,
                        title_height=0, title_space=0,
                        # Turn off the endnote/title axis. I usually do this after
                        # I am happy with the chart layout and text placement
                        axis=False,
                        grid_height=0.8)
    fig.set_facecolor('white')

    # heatmap and labels
    bin_statistic = pitch.bin_statistic_positional(evento.x, evento.y, statistic='count',
                                                positional='full', normalize=True)
    pitch.heatmap_positional(bin_statistic, ax=axs['pitch'],
                            cmap=pearl_earring_cmap, edgecolors='#245D93')
    labels = pitch.label_heatmap(bin_statistic, color='#f4edf0', fontsize=18,
                                ax=axs['pitch'], ha='center', va='center',
                                str_format='{:.0%}', path_effects=path_eff)


    st.pyplot(fig)

def ajuste_margenes():
    st.markdown("""
        <style>
            .main .block-container {
                padding-top: 2rem;  /* Ajustar margen superior */
                padding-bottom: 2rem;  /* Ajustar margen inferior */
                margin-left: -2rem;  /* Ajustar margen izquierdo */
                margin-right: -3rem;  /* Ajustar margen derecho */
            }
        </style>
    """, unsafe_allow_html=True)

def diseno_boton():
    st.markdown("""
    <style>
    .stButton:nth-child(1) button {
        background-color: #0a0a0a;  /* Color para el primer botón */
        color: white;
        border-radius: 8px;
        padding: 10px;
        font-size: 20px;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

def mostrar_marcador(partido, equipo_local, equipo_visitante):
    html_code = f"""
            <div style="display: flex; justify-content: center; align-items: center; background-color: #227c9e; padding: 10px; border-radius: 10px; max-width: 500px; margin: auto;margin-left: 230px">
                <div style="flex: 1; text-align: center; color: white; font-weight: bold;">
                    <! <img src="https://img.icons8.com/ios-glyphs/30/ffffff/soccer-ball.png" style="vertical-align: middle;"/>
                    {equipo_local}
                </div>
                <div style="background-color: #4f9bb8; color: white; font-size: 24px; padding: 10px 20px; border-radius: 10px; margin: 0 10px;">
                    <span style="font-weight: bold;">{partido['home_score']} - {partido['away_score']}</span>
                </div>
                <div style="flex: 1; text-align: center; color: white; font-weight: bold;">
                    {equipo_visitante}
                    <! <img src="https://img.icons8.com/ios-glyphs/30/ffffff/soccer-ball.png" style="vertical-align: middle;"/>
                </div>
            </div>
            """
            # Muestra el marcador en Streamlit
    st.markdown(html_code, unsafe_allow_html=True)

def grafica_formaciones(formaciones, equipo):
    if equipo == 'Local':
        formacion = formaciones['tactics'][0]
    elif equipo == 'Visitante':
        formacion = formaciones['tactics'][1]
    formation = str(int(formacion['formation']))
    positions = [player["position"]["id"] for player in formacion["lineup"]]
    text = [player["player"]["id"] for player in formacion["lineup"]]

    pitch = VerticalPitch(goal_type='box', pitch_color='grass')
    fig, ax = pitch.draw(figsize=(6.875, 10))
    position_text = pitch.formation(formation,
                                    positions=positions,
                                    text=text,
                                    ax=ax,
                                    kind='scatter', s=450,
                                    color='#4f9bb8')
    st.write(formation)
    st.pyplot(fig)

    return positions, text

def calcular_posesion(eventos,equipo_local, equipo_visitante):
    posesion = eventos.dropna(subset='duration')
    posesison_time = posesion.groupby('team').agg({'duration':'sum'}).sort_values('duration',ascending=False)
    total_time = posesison_time.sum()
    posesion_pct = (posesison_time / total_time) * 100

    posesion_equipo_local = posesion_pct.loc[equipo_local, 'duration'] if equipo_local in posesion_pct.index else 0
    posesion_equipo_visitante = posesion_pct.loc[equipo_visitante, 'duration'] if equipo_visitante in posesion_pct.index else 0

    posesion_equipo_local = f"{posesion_equipo_local:.1f}%"
    posesion_equipo_visitante = f"{posesion_equipo_visitante:.1f}%"

    return posesion_equipo_local, posesion_equipo_visitante

def goles_esperados(eventos, equipo_local, equipo_visitante):
    tiros = eventos[eventos['type']=='Shot']
    tiros.dropna(axis=1, how='all',inplace=True)
                
    goles_esperados = tiros.groupby('team').agg({'shot_statsbomb_xg':'sum'}).sort_values('shot_statsbomb_xg',ascending=False)
    goles_esperados_local = goles_esperados.loc[equipo_local, 'shot_statsbomb_xg'] if equipo_local in goles_esperados.index else 0
    goles_esperados_visitante = goles_esperados.loc[equipo_visitante, 'shot_statsbomb_xg'] if equipo_visitante in goles_esperados.index else 0
    goles_esperados_local = f"{goles_esperados_local:.2f}"
    goles_esperados_visitante = f"{goles_esperados_visitante:.2f}"
    return goles_esperados_local, goles_esperados_visitante

def total_remates(eventos,equipo_local, equipo_visitante):
    tiros = eventos[eventos['type']=='Shot']
    tiros.dropna(axis=1, how='all',inplace=True)
    remates = tiros.groupby(['team']).agg({'index':'count'})
    remates_local = remates.loc[equipo_local, 'index'] if equipo_local in remates.index else 0
    remates_visitante = remates.loc[equipo_visitante, 'index'] if equipo_visitante in remates.index else 0
    return remates_local, remates_visitante    

def remates_al_arco(eventos, equipo_local, equipo_visitante):
    tiros = eventos[eventos['type']=='Shot']
    tiros.dropna(axis=1, how='all',inplace=True)
    tiros_arco = tiros[tiros['shot_outcome'].isin(['Goal','Saved','Saved To Post'])]
    tiros_arco = tiros_arco.groupby(['team']).agg({'index':'count'})
    remates_arco_local = tiros_arco.loc[equipo_local, 'index'] if equipo_local in tiros_arco.index else 0
    remates_arco_visitante = tiros_arco.loc[equipo_visitante, 'index'] if equipo_visitante in tiros_arco.index else 0
    return remates_arco_local, remates_arco_visitante

def tiros_esquina(eventos, equipo_local, equipo_visitante):
    pases = eventos[eventos['type']=='Pass']
    corners = pases[pases['pass_type']=='Corner']
    corners = corners.groupby(['team']).agg({'index':'count'})
    corners_local = corners.loc[equipo_local, 'index'] if equipo_local in corners.index else 0
    corners_visitante = corners.loc[equipo_visitante, 'index'] if equipo_visitante in corners.index else 0
    return corners_local, corners_visitante

def offsides(eventos, equipo_local, equipo_visitante):
    pases = eventos[eventos['type']=='Pass']
    offsides = pases[pases['pass_outcome']=='Pass Offside']
    offsides = offsides.groupby(['team']).agg({'index':'count'})
    offsides_local = offsides.loc[equipo_local, 'index'] if equipo_local in offsides.index else 0
    offsides_visitante = offsides.loc[equipo_visitante, 'index'] if equipo_visitante in offsides.index else 0
    return offsides_local, offsides_visitante

def pases_completados(eventos, equipo_local, equipo_visitante):
    pases = eventos[eventos['type'] == 'Pass']
    pases_completados = pases[pases['pass_outcome'].isnull()]
    # Total de pases intentados
    total_pases = pases.groupby('team').agg({'index': 'count'})
    pases_completados = pases_completados.groupby('team').agg({'index': 'count'})
    # Obtener valores para cada equipo
    total_pases_local = total_pases.loc[equipo_local, 'index'] if equipo_local in total_pases.index else 0
    total_pases_visitante = total_pases.loc[equipo_visitante, 'index'] if equipo_visitante in total_pases.index else 0

    pases_completados_local = pases_completados.loc[equipo_local, 'index'] if equipo_local in pases_completados.index else 0
    pases_completados_visitante = pases_completados.loc[equipo_visitante, 'index'] if equipo_visitante in pases_completados.index else 0

    # Calcular % de pases completados
    pct_completados_local = (pases_completados_local / total_pases_local * 100) if total_pases_local > 0 else 0
    pct_completados_visitante = (pases_completados_visitante / total_pases_visitante * 100) if total_pases_visitante > 0 else 0
    pct_completados_local = f"{pct_completados_local:.1f}%"
    pct_completados_visitante = f"{pct_completados_visitante:.1f}%"
    return pases_completados_local, pct_completados_local, pases_completados_visitante, pct_completados_visitante