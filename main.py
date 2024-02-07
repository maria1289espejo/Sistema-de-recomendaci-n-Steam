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
# Carga los archivos para realizar consultas
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
    # Revisa si el desarrollador esta en la columna developer´de df_data_games
    if desarrollador in df_data_games['developer'].str.lower().values:
        # Filtra la columna por desarrollador
        df_desarrollador = df_data_games[df_data_games['developer'].str.lower() == desarrollador]
        # Convierte 'release_date' a datetime
        df_desarrollador['release_date'] = pd.to_datetime(df_desarrollador['release_date'])
        # Agrupa por año y cuenta el número de id únicos y gratuitos
        resultados_por_año = df_desarrollador.groupby(df_desarrollador['release_date'].dt.year)[['id', 'price']].nunique()
        # Calcula porcentaje de items gratuitos
        porcentaje_items_free = (df_desarrollador['price'] == 0).mean() * 100
        # Agrega columna de porcentajes a resultados por año
        resultados_por_año[porcentaje_items_free] = porcentaje_items_free
        # Renombra columnas
        resultados_por_año = resultados_por_año.rename(columns={'id': 'Cantidad de items', 0.0: '% Contenido free'})
        # Organiza formato de la respuesta
        respuesta = resultados_por_año.drop(columns='price').to_dict(orient='index')
    else:  respuesta = f"{desarrollador} no está disponible, intenta con otro desarrollador."

    return respuesta

@app.get("/userdata/{User_id}")
def userdata(User_id: str):

    # Convierte User_id a cadena de caracteres
    User_id = str(User_id)    
    # Verifica si user_id está en la columna user_id de df_data_items
    if User_id in df_data_items['user_id'].unique():
        # Filtra df_data_items por el user_id específico
        usuario_filtrado_items = df_data_items[df_data_items['user_id'] == User_id]
        # Obtine el valor de items_count para el user_id dado
        items_cantidad = usuario_filtrado_items['items_count'].iloc[0]
        # Obtiene los item_id de los juegos usados para el user_id dado
        item_id_usados = usuario_filtrado_items['item_id'].tolist()
        # Selecciona la columna price de df_data_games
        precios_games = df_data_games[['id','price']]
        # Une usuario_filtrado_items con precios_games
        usuario_filtrado_items = pd.merge(usuario_filtrado_items, precios_games, left_on='item_id', right_on='id', how='inner')
        # Suma el dinero gastado
        dinero_gastado = usuario_filtrado_items['price'].sum()
        # Filtra df_data_reviews por el user_id específico
        usuario_filtrado_reviews = df_data_reviews[df_data_reviews['user_id'] == User_id]
        # Cuenta cantidad de juegos recomendados o no por usuario
        recommend_cantidad = usuario_filtrado_reviews['recommend'].count()
        # Calcula porcentaje de recomendación
        porcentaje_recomendación = recommend_cantidad*100/items_cantidad
        # Organiza formato de la respuesta
        respuesta = f"Usuario: {User_id}, Dinero gastado: {dinero_gastado} USD, % de recomendación: {porcentaje_recomendación:.2f} %, Cantidad de items: {items_cantidad}"
    else:
        respuesta = f"Usuario: {User_id} no está disponible. Intenta con otro id de usuario."
        
    return respuesta

@app.get("/UserForGenre/{genero}")
def UserForGenre( genero : str ):

    genero = genero.lower()
    # Verifica si el género está en la columna genero de df_data_games
    if genero in df_data_games['genres'].str.lower().values:
        # Filtra el dataframe por el género dado
        df_genero = df_data_games[df_data_games['genres'].str.lower() == genero]
        # Selecciona las columnas item_id y playtime_forever de df_data_items
        seleccion_df_items = df_data_items[['item_id', 'user_id', 'playtime_forever']]
        # Une df_genero y seleccion_items
        df_genero = pd.merge(df_genero, seleccion_df_items, left_on='id', right_on='item_id', how='inner')
        # Convierte 'release_date' a datetime
        df_genero['release_date'] = pd.to_datetime(df_genero['release_date'])
        # Agrupa por año y sumar las horas de juego
        acumulacion_horas_por_año = df_genero.groupby(df_genero['release_date'].dt.year)['playtime_forever'].sum()
        # Obtiene el usuario que acumula más horas jugadas
        usuario_max_horas_jugadas = df_genero.groupby('user_id')['playtime_forever'].sum().idxmax()
        # Organiza formato de la respuesta
        respuesta = {
            'usuario_max_horas_jugadas': usuario_max_horas_jugadas,
            'acumulacion_horas_por_año': acumulacion_horas_por_año.to_dict()
        }
    else:
        respuesta = f"El género {genero} no está disponible, intente con otro género" 

    return respuesta

@app.get("/best_developer_year/{anio}")
def best_developer_year(año : int):
    
    # Verifica que el año este en la columna posted de df_data reviews
    if año in (pd.to_datetime(df_data_reviews['posted'], yearfirst= True).dt.year).values:
        # Filtra por el dataframe por el año indicado
        df_año = df_data_reviews[pd.to_datetime(df_data_reviews['posted'], yearfirst=True).dt.year == año]
        # Selecciona columna developer de df_data_games
        df_desarrollador = df_data_games[['id', 'developer']]
        # Une df_año y df_desarrollador
        df_año_desarrollador = pd.merge(df_año, df_desarrollador, left_on='item_id', right_on='id', how='inner')
        # Cuenta cantidad de True en recommend por desarrollador
        contar_true = df_año_desarrollador.groupby('developer')['recommend'].apply(lambda x: (x == 'True').sum()).reset_index(name='conteo_recomendados')
        # Cuenta cantidad de reseñas positivas por desarrollador
        contar_positivas = df_año_desarrollador.groupby('developer')['sentiment_analysis'].apply(lambda x: (x == 2).sum()).reset_index(name='conteo_positivas')
        # Une contar positivas con contar true
        contar_true_positivas = pd.merge(contar_true, contar_positivas, on='developer', how='inner')
        # Da orden descendente a contar_tru_positivas
        top_recomendados = contar_true_positivas.sort_values('conteo_positivas', ascending=False).head(3)
        # Organiza formato de la respuesta
        respuesta = f"Puesto 1: {top_recomendados['developer'].iloc[0]}, Puesto 2: {top_recomendados['developer'].iloc[1]}, Puesto 3: {top_recomendados['developer'].iloc[2]}"
    else:
        respuesta = f"El {año} no esta disponible, intente con otro año"   

    return respuesta

@app.get("/developer_reviews_analysis/{desarrollador}")
def developer_reviews_analysis( desarrollador : str ):

    desarrollador = desarrollador.lower()
    # Verifica si el desarrollador está en la columna 'developer' de df_data_games
    if desarrollador in df_data_games['developer'].str.lower().values:
        # Filtra la columna por desarrollador
        df_desarrollador = df_data_games[df_data_games['developer'].str.lower() == desarrollador]
        # Une df_desarrollador y df_data_reviews en base a 'id' e 'item_id'
        df_desarrollador = pd.merge(df_desarrollador, df_data_reviews[['item_id', 'sentiment_analysis']], left_on='id', right_on='item_id', how='inner') 
        # Revisa si el dataframe generado esta vacio
        if df_desarrollador.empty:
            # Organiza formato de la respuesta
            respuesta = {desarrollador: ['Negative = 0', 'Positive = 0']}
        else:
            # Cuenta la cantidad de ocurrencias de cada valor de 'sentiment_analysis'
            conteo_de_valores = df_desarrollador['sentiment_analysis'].value_counts()
            # Obtiene la cantidad de ocurrencias de 0 y 2, si no hay, devolver 0
            cantidad_negativas = conteo_de_valores.get(0, 0)
            cantidad_positivas = conteo_de_valores.get(2, 0)
            # Crea el diccionario de respuesta
            respuesta = {desarrollador: [f'Negative = {cantidad_negativas}', f'Positive = {cantidad_positivas}']}
    else:
        respuesta = {desarrollador: ['Negative = 0', 'Positive = 0']}

    return respuesta

# Sistema de recomendación

@app.get("/obtener_recomendaciones/{item_id}")
def obtener_recomendaciones(item_id: int):

    # Verifica si item_id esta en df_data_reviews
    if item_id in df_data_reviews['item_id']:
        # Filtra el DataFrame para obtener solo las filas relacionadas con el item_id proporcionado
        item_actual = df_data_reviews[df_data_reviews['item_id'] == item_id]
        # Filtra el DataFrame para excluir el item_id proporcionado
        df_sin_item_actual = df_data_reviews[df_data_reviews['item_id'] != item_id]
        # Selecciona solo la columna de género del DataFrame df_genero
        df_data_games_seleccionado = df_data_games[['id', 'genres']]
        # Une el DataFrame de género al DataFrame principal
        df_sin_item_actual = pd.merge(df_sin_item_actual, df_data_games_seleccionado, left_on='item_id', right_on='id', how='inner')
        # Elimina la columna redundante 'id'
        df_sin_item_actual = df_sin_item_actual.drop('id', axis=1) 
        # Obtiene el género del item actual
        genero_actual = df_data_games[df_data_games['id'] == item_id]['genres'].values[0]

        # Calcula la similitud basada en recommend, sentiment_analysis y género
        similarities = []
        for index, row in df_sin_item_actual.iterrows():
            similarity = (item_actual['recommend'].values[0] == row['recommend']) and \
                          (item_actual['sentiment_analysis'].values[0] == row['sentiment_analysis']) and \
                          (genero_actual == row['genres'])
            similarities.append(similarity)
        # Obtiene los índices de los items más similares
        indices_similares = [i for i, x in enumerate(similarities) if x]
        # Obtiene los item_id correspondientes a los índices encontrados
        items_similares = df_sin_item_actual.loc[indices_similares, 'item_id'].tolist()
        # Obtiene los titulos correspondientes
        juegos_similares = df_data_games[df_data_games['id'].isin(items_similares)]['title']
        # Elimina duplicados
        juegos_similares = juegos_similares.drop_duplicates().head(5).to_list()
        # Organiza formato de la respuesta
        respuesta =  juegos_similares        
    else: respuesta = f"{item_id} no está disponible, intenta con otro item_id."

    return respuesta  