import pandas as pd
import mysql.connector as sql

def leer_partidos():
    user = 'root'
    password = ''
    host = '127.0.0.1'  # Cambia si es un servidor remoto
    database = 'laliga_15_16'
    db_connection = sql.connect(user=user, password=password, host=host, database=database)
    partidos = pd.read_sql(f"""SELECT * 
                                FROM partidos                 
                                    """ , con=db_connection)
    return partidos

def leer_jugdores(lista_ids):
    user = 'root'
    password = ''
    host = '127.0.0.1'  # Cambia si es un servidor remoto
    database = 'laliga_15_16'
    db_connection = sql.connect(user=user, password=password, host=host, database=database)
    query = """SELECT player_id, player_nickname, player_name 
                                FROM jugadores
                                WHERE player_id in %s"""
    jugadores = pd.read_sql(query % str(tuple(lista_ids)), con=db_connection) 
    return jugadores