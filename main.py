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
#from sklearn.metrics.pairwise import cosine_similarity


# Pone nombre, descripción y versión a la API
app = FastAPI(title='Juegos recomendados',
              description='Sistema de recomendación de juegos de la plataforma Steam basado en tus gustos',
              version='1.0')

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
#similarity_matrix_recuperada = np.load(file_path_similarity_matrix)

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

# Modelo de aprendizaje

# Calcula la matriz de similitud de coseno directamente sobre la columna de Sentimiento
#similarity_matrix = cosine_similarity(df_data_reviews[['sentiment_analysis']], df_data_reviews[['sentiment_analysis']])


# Sistema de recomendación item-item:
#@app.get("/recomendacion_juego/{item_id}")
#def obtener_recomendaciones(item_id: int):
    n = 5
    # Obtiene el índice del juego en df_data_reviews
    #index_df_data_reviews = df_data_reviews[df_data_reviews['item_id'] == item_id].index[0]

    # Obtiene la fila correspondiente en la matriz de similitud
    #similar_scores = list(enumerate(similarity_matrix[index_df_data_reviews]))

    # Ordena los juegos por similitud
    #similar_scores = sorted(similar_scores, key=lambda x: x[1], reverse=True)

    # Obtiene los índices de los juegos similares
    #top_indices = [i[0] for i in similar_scores[1:]]

    # Obtiene los item_id de los juegos recomendados
    #recommendados_item_ids = df_data_reviews['item_id'].iloc[top_indices]

    # Obtiene los nombres (titles) de los juegos recomendados desde df_data_games
    #recommendados_juegos = df_data_games[df_data_games['id'].isin(recommendados_item_ids)]['title']

    # Elimina duplicados
    #recommendados_juegos = recommendados_juegos.drop_duplicates().head(n)

    #return recommendados_juegos