# Librerias a utilizar
from fastapi import FastAPI, HTTPException
from typing import List, Dict
import pandas as pd
from datetime import datetime
from fastparquet import ParquetFile
from unidecode import unidecode
from pydantic import BaseModel
import uvicorn
import os
import numpy as np

# Obtiene el directorio actual del archivo
current_directory = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()

# Construye la ruta al archivo de datos en la carpeta 'dataset_limpios'
file_path_reviews_sentiment = os.path.join(current_directory, "datasets_post_limpieza", "df_reviews_sentiment.parquet.gzip")
file_path_items = os.path.join(current_directory, "datasets_post_limpieza", "df_items_clean.parquet.gzip")
file_path_games = os.path.join(current_directory, "datasets_post_limpieza", "df_games_clean.parquet.gzip")
#file_path_similarity_matrix = os.path.join(current_directory, "datasets_post_limpieza", "similarity_matrix.npz")
# Cargar los archivos para realizar consultas
data_reviews = ParquetFile(file_path_reviews_sentiment)
df_data_reviews = data_reviews.to_pandas()
data_items = ParquetFile(file_path_items)
df_data_items = data_items.to_pandas()
data_games = ParquetFile(file_path_games)
df_data_games = data_games.to_pandas()


# Pone nombre, descripción y versión a la API
app = FastAPI(title='Juegos recomendados',
              description='Sistema de recomendación de juegos de la plataforma Steam basado en tus gustos',
              version='1.0')


# End point de prueba
@app.get("/")
def read_root():
    return {"Bienvenido al sistema de recomendación de juegos"}


@app.get("/developer/{desarrollador}")
def developer(desarrollador: str):
    # Convierte la entrada a minisculas
    desarrollador = desarrollador.lower()
    # revisa si el desarrollador esta en la columna developer´de df_data_games
    if desarrollador in df_data_games['developer'].str.lower().values:
        # filtra la columna por desarrollador
        df_desarrollador = df_data_games[df_data_games['developer'].str.lower() == desarrollador]
        # Convertir 'release_date' a datetime
        df_desarrollador['release_date'] = pd.to_datetime(df_desarrollador['release_date'])
        # Agrupar por año y contar el número de id únicos y gratuitos
        resultados_por_año = df_desarrollador.groupby(df_desarrollador['release_date'].dt.year)[['id', 'price']].nunique()
        # Calcula porcentaje de items gratuitos
        porcentaje_items_free = (df_desarrollador['price'] == 0).mean() * 100
        resultados_por_año[porcentaje_items_free] = porcentaje_items_free
        resultados_por_año = resultados_por_año.rename(columns={'id': 'Cantidad de items', 0.0: '% Contenido free'})

        respuesta = resultados_por_año.drop(columns='price').to_dict(orient='index')
    else:  respuesta = f"{desarrollador} no está disponible, intenta con otro desarrollador."

    return respuesta

@app.get("/userdata/{User_id}")
def userdata( User_id : str ):
    return {"En proceso"}

@app.get("/UserForGenre/{genero}")
def UserForGenre( genero : str ):
    return {"En proceso"}

@app.get("/best_developer_year/{anio}")
def best_developer_year( año : int ):
    return {"En proceso"}

@app.get("/developer_reviews_analysis/{desarrollador}")
def developer_reviews_analysis( desarrolladora : str ):
    return {"En proceso"}

@app.get("/obtener_recomendaciones/{item_id}")
def obtener_recomendaciones(item_id: int):
    # verifica si item_id esta en df_data_reviews
    if item_id in df_data_reviews['item_id']:
        # Filtrar el DataFrame para obtener solo las filas relacionadas con el item_id proporcionado
        item_actual = df_data_reviews[df_data_reviews['item_id'] == item_id]
        # Filtrar el DataFrame para excluir el item_id proporcionado
        df_sin_item_actual = df_data_reviews[df_data_reviews['item_id'] != item_id]
        # Seleccionar solo la columna de género del DataFrame df_genero
        df_data_games_seleccionado = df_data_games[['id', 'genres']]
        # Unir el DataFrame de género al DataFrame principal
        df_sin_item_actual = pd.merge(df_sin_item_actual, df_data_games_seleccionado, left_on='item_id', right_on='id', how='inner')
        # Eliminar la columna redundante 'id'
        df_sin_item_actual = df_sin_item_actual.drop('id', axis=1) 
        # Obtener el género del item actual
        genero_actual = df_data_games[df_data_games['id'] == item_id]['genres'].values[0]
        # Calcular la similitud basada en recommend, sentiment_analysis y género
        similarities = []
        for index, row in df_sin_item_actual.iterrows():
            similarity = (item_actual['recommend'].values[0] == row['recommend']) and \
                          (item_actual['sentiment_analysis'].values[0] == row['sentiment_analysis']) and \
                          (genero_actual == row['genres'])
            similarities.append(similarity)

        # Obtener los índices de los items más similares
        indices_similares = [i for i, x in enumerate(similarities) if x]
        # Obtener los item_id correspondientes a los índices encontrados
        items_similares = df_sin_item_actual.loc[indices_similares, 'item_id'].tolist()
        juegos_similares = df_data_games[df_data_games['id'].isin(items_similares)]['title']
        #Elimina duplicados
        juegos_similares = juegos_similares.drop_duplicates().head(5).to_list()
        respuesta =  juegos_similares
        
    else: respuesta = f"{item_id} no está disponible, intenta con otro item_id."
    return respuesta  