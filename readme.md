# <p align="center">Proyecto Sistema de Recomendación</p>

## Descripción

El proposito del presente proyecto es crear una API donde se puedean consumir los datos y el sistema de recomendación creado a partir de estos por medio de funciones, esta Api debe ser accesible desde la web. Si bien no se piden transformaciones especificas, si se realizaron transformaciones para poder acceder facilmente a los datos, ya que los datos originales estaban anidados, se eliminaron datos que no aportaban información relevante ya fuera porque no eran necesarios para las funciones o porque eran nulos, posteriormente se realizó un analisis exploratorio para observar el comportamiento y distribuón de los datos y por ultimo se creo y disponibilizo en la web la API.

## Tecnologías Utilizadas

Transformación, limpieza, EDA, ingeniería de características, funciones y modelo de aprendizaje fueron realizados con Python 3.10.4 en Visual Studio Code 1.86.0. Las librerás utilizadas en cada etapa son las siguientes:

### Transformación y limpieza

- dask
- dask.dataframe
- pandas
- pyarrow.json
- gzip
- json
- ast

### Análisis exploratorio de datos (EDA)

- dask.dataframe
- pandas
- numpy
- seaborn
- matplotlib.pyplot
- scipy.stats
- datetime
- os

### Ingeniería de características (Feature Engineering)

- pandas
- textblob
- nltk.sentiment
- os

### Funciones y modelo de aprendizaje

- fastapi
- typing
- pandas
- datetime
- fastparquet
- unidecode
- pydantic
- uvicorn
- os
- numpy

API fue realizada por medio de FastAPI con interfaz openapi 3.1.0 y disponibilizada con Render.

## ETL y Proceso de Datos

### Limpieza y transformación inicial

Los [datos utilizados](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj) son datos publicos de la plataforma de videojuegos Steam, estos estaban distribuidos en tres archivos en formato .json.gz los cuales tenian tamaños superiores a los 2500 kb cada uno; para poder tener estos datos, en un formato facil de visualizar se utilizó la biblioteca dask, ya que esta permite leer archivos de gran tamaño mediante ejecución paralela y alta capacidad de memoria.

El proceso comenzó con una revisión del [diccionario de datos](https://docs.google.com/spreadsheets/d/1-t9HLzLHIGXvliq56UE_gMaWBVTPfrlTf2D9uAtLGrk/edit#gid=0), las consultas propuestas y los datos visibles. Se identificaron las columnas necesarias y se eliminaron aquellas que no eran relevantes. Luego, se procedió a eliminar las filas que contenían valores nulos en todas las columnas y las duplicadas.

Durante la exploración de un fragmento de los datos, se observó que varías columnas estaban anidadas, como la columna genres del archivo steam_games, se determinó la estructura de estas anidaciones y se crearon funciones para desanidarlas. Posteriormente se guardaron los datos en formato .parquet.gzip, dado que este formato es liviano y facil de leer, estos archivos estan disponibles en la carpeta [datasets_post_limpieza](https://github.com/maria1289espejo/Sistema-de-recomendaci-n-Steam/tree/main/datasets_post_limpieza)

### Análisis exploratorio de datos EDA

Se revisó de manera más detallada los dataframe, describiendo la cantidad de columnas, filas, el contenido, el tipo de datos, la cantidad de datos nulos; en algunas columnas fue necesario cambiar el tipo de datos y eliminar algunos datos que se consideraron innecesarios. Seguidamente se realizó un análisis descriptivo de los datos, se observó la distribución de algunas variables categóricas y algunas variables cuantitativas para conocer el comportamiento de los datos, los gráficos y observaciones correspondientes pueden verse en el archivo [EDA.ipny](https://github.com/maria1289espejo/Sistema-de-recomendaci-n-Steam/blob/main/notebooks/EDA.ipynb) de la carpeta notebooks.

## API y Sistema de Recomendación

## Deployment

## Uso y Ejemplos

## Estado del Proyecto

## Contacto

[Linkedink](https://www.linkedin.com/in/alejandra-monroy-e/)

[Correo](mailto:maria1289espejo@gmail.com)

## Referencias
