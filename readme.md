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

Además de las tecnologías mencionadas anteriormente, se utilizó el software de grabación OBS Studio para crear el video explicativo que muestra como funciona la API.

## ETL y Proceso de Datos

### Limpieza y transformación inicial

Los [datos utilizados](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj) son datos publicos de la plataforma de videojuegos Steam, estos estaban distribuidos en tres archivos en formato .json.gz los cuales tenian tamaños superiores a los 2500 kb cada uno; para poder tener estos datos, en un formato facil de visualizar se utilizó la biblioteca dask, ya que esta permite leer archivos de gran tamaño mediante ejecución paralela y alta capacidad de memoria.

El proceso comenzó con una revisión del [diccionario de datos](https://docs.google.com/spreadsheets/d/1-t9HLzLHIGXvliq56UE_gMaWBVTPfrlTf2D9uAtLGrk/edit#gid=0), las consultas propuestas y los datos visibles. Se identificaron las columnas necesarias y se eliminaron aquellas que no eran relevantes. Luego, se procedió a eliminar las filas que contenían valores nulos en todas las columnas y las duplicadas.

Durante la exploración de un fragmento de los datos, se observó que varías columnas estaban anidadas, como la columna genres del archivo steam_games, se determinó la estructura de estas anidaciones y se crearon funciones para desanidarlas. Posteriormente se guardaron los datos en formato .parquet.gzip, dado que este formato es liviano y facil de leer, estos archivos estan disponibles en la carpeta [datasets_post_limpieza](https://github.com/maria1289espejo/Sistema-de-recomendaci-n-Steam/tree/main/datasets_post_limpieza).

### Análisis exploratorio de datos

Se revisó de manera más detallada los dataframe, describiendo la cantidad de columnas, filas, el contenido, el tipo de datos, la cantidad de datos nulos; en algunas columnas fue necesario cambiar el tipo de datos y eliminar algunos datos que se consideraron innecesarios. Seguidamente se realizó un análisis descriptivo de los datos, se observó la distribución de algunas variables categóricas y algunas variables cuantitativas para conocer el comportamiento de los datos, los gráficos y observaciones correspondientes pueden verse en el archivo [EDA.ipny](https://github.com/maria1289espejo/Sistema-de-recomendaci-n-Steam/blob/main/notebooks/EDA.ipynb) de la carpeta notebooks.

### Ingenieria de características

Se llevó a cabo un análisis de sentimiento en la columna review del archivo reviews previamente  procesado. Este análisis clasifica las reseñas como negativas, neutras o positivas. Para lograrlo, se desarrolló una función que analiza el texto de cada fila y calcula la polaridad de la reseña. La polaridad es un valor entre -1 y 1, donde -1 representa una reseña totalmente negativa y 1 una reseña totalmente positiva. Luego, se asigna un valor específico: 0 para polaridades menores a 0, 1 para polaridades iguales a 0 y 2 para polaridades mayores a 0. La función esta disponible en el archivo [feature engineering](https://github.com/maria1289espejo/Sistema-de-recomendaci-n-Steam/blob/main/notebooks/feature%20engineering.ipynb) de la carpeta notebooks.

## API y Sistema de Recomendación

Se desarrolaron varias funciones que permiten consumir los datos y el modelo de aprendizaje. Cada función está decorada con `@app.get`, lo que crea un botón para acceder a la función correspondiente. Estas funciones reciben datos de entrada y devuelven un mensaje de salida, según lo programado en el retorno de la función.

El sistema de recomendación implementado es un modelo item-item, basado en la similitud del análisis de sentimiento de las reseñas, la percepción del usuario sobre la recomendación del juego y su género. La función genera un listado en orden descendente de similitud de los 5 juegos más similares al ingresado.

Todas las funciones pueden ser visualizadas en el archivo [main.py](https://github.com/maria1289espejo/Sistema-de-recomendaci-n-Steam/blob/main/main.py). Este archivo debe ubicarse en la carpeta raíz.

Una vez que las funciones fueron creadas, en la terminal del editor se ejecutó el comando `uvicorn main:app --reload`, el cual proporciona un enlace local para poder visualizar y utilizar la API en el explorador web.

## Deployment

Se creó un archivo .gitignore utilizando un editor de texto, en el cual se especificaron las rutas de los archivos y carpetas que, aunque forman parte del proyecto, no se necesitan subir a GitHub; como `_pycache_` y `venv`.

Luego, se procedió a crear un entorno virtual en la carpeta raíz del proyecto utilizando la consola del sistema. Este entorno virtual es necesario para que, al ejecutar la API, el servidor disponga de los programas y librerías necesarias para su funcionamiento. Estando dentro del entorno virtual se ejecutó el comando `pip freeze > requirements.txt` para crear un archivo llamado requirements.txt que contiene sola las librerias utilizadas en el proyecto, despues se cerro el entorno virtual.

Se creó un repositorio nuevo en GitHub, y se subio la carpeta local del proyecto a la plataforma desde la terminal del editor, una vez disponible en Github los archivos del proyecto, se abrió una cuenta en Render.com y se creo un web services enlazado al repositorio de GitHub, cuando la plataforma indico que el deploy fue exitoso se generó este [link](https://api-steam-juegos-recomendados-3h5d.onrender.com/) en el cual se puede acceder a la API desde un navegador web.

## Uso y Ejemplos

Se realizó un [video](https://youtu.be/vA05xt5sSKA) que explica el funcionamiento de la API y proporciona ejemplos de entradas y sus correspondientes respuestas.

## Estado del Proyecto

## Contacto

[Linkedink](https://www.linkedin.com/in/alejandra-monroy-e/)

[Correo](mailto:maria1289espejo@gmail.com)
