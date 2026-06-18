# TP_Aplicado: CineMood 🎬

## Integrantes
* Sofia Moreno Coppa Oliver
* Carmin Bausili 
* Malena Cirolini

------------------------------------------------------------------------------------------------------------------------------------------------
## Objetivo del proyecto

CineMood es un sistema de recomendación de películas basado en estados emocionales. El objetivo es ayudar a los usuarios a encontrar películas acordes a cómo se sienten en un momento determinado. A diferencia de los sistemas tradicionales de recomendación, que suelen basarse en géneros o popularidad, CineMood utiliza un cuestionario para inferir un perfil emocional y generar recomendaciones personalizadas.

------------------------------------------------------------------------------------------------------------------------------------------------
## Descripción general del funcionamiento

El programa realiza un cuestionario compuesto por cuatro preguntas relacionadas con el estado emocional del usuario.
A partir de las respuestas:

1. Se infiere un estado emocional.
2. Se filtra un dataset de aproximadamente 2000 películas obtenido desde la API de TMDB.
3. Se calcula un porcentaje de compatibilidad para cada película.
4. Se genera un ranking personalizado.
5. Se muestran gráficos de análisis.
6. Se registra la película elegida por el usuario.
7. Se muestran recomendaciones colaborativas basadas en elecciones previas.

------------------------------------------------------------------------------------------------------------------------------------------------
## Funciones principales

### cuestionario.py
* pedir_numero(): valida que el usuario ingrese un número entre 1 y 10.
* hacer_cuestionario(): realiza el cuestionario emocional interactivo.
* inferir_estado(): determina el perfil emocional del usuario a partir de sus respuestas.

### recomendador.py
* filtrar(): selecciona las películas compatibles con el perfil emocional.
* calcular_match(): calcula el porcentaje de compatibilidad de cada película.
* pedir_si_no(): valida respuestas de tipo sí/no.
* recomendar_hasta_elegir(): muestra recomendaciones hasta que el usuario elija una película.
* pedir_eleccion(): registra la película seleccionada por el usuario.

### colaborativo.py
* guardar_eleccion(): almacena la elección realizada en el historial colaborativo.
* mostrar_colaborativo(): muestra películas elegidas previamente por usuarios con perfiles similares.

### graficos.py
* contar_generos(): contabiliza la frecuencia de géneros en las coincidencias encontradas.
* mostrar_grafico_generos(): genera un gráfico de géneros más frecuentes.
* cargar_poster(): descarga y carga posters desde TMDB.
* mostrar_grafico(): genera un gráfico de compatibilidad con posters de películas.
* mostrar_grafico_rating(): muestra las películas ordenadas por rating.
* mostrar_grafico_decadas(): visualiza la distribución de coincidencias por década.

### df_api.py
* pedir_datos(): realiza consultas a la API de TMDB.
* obtener_ids_top_rated(): obtiene los identificadores de las películas mejor valoradas.
* obtener_detalle_pelicula(): recupera la información detallada de una película.
* crear_dataframe_top_rated(): construye el dataset utilizado por el sistema.
* main(): genera y exporta el dataset completo a formato CSV.

------------------------------------------------------------------------------------------------------------------------------------------------
## Adjudicación de tareas

### Sofía Moreno Coppa Oliver

* Desarrollo del cuestionario emocional.
* Implementación de la lógica para determinar el perfil emocional del usuario.
* Organización del repositorio en GitHub.
* Redacción y actualización del README.
* Integración general de las distintas partes del proyecto.

### Carmin Bausili

* Diseño de los diagramas de flujo y documentación visual.
* Análisis del funcionamiento general del sistema.
* Pruebas y validación de resultados.
* Colaboración en la definición de la estructura del proyecto.

### Malena Cirolini

* Integración con la API de TMDB.
* Obtención y procesamiento de los datos de películas.
* Generación del dataset utilizado por el sistema.
* Desarrollo de los gráficos y visualizaciones.
* Implementación de la carga y visualización de posters.

------------------------------------------------------------------------------------------------------------------------------------------------
## Fuente de datos

Para este proyecto se utilizó la API pública de TMDB (The Movie Database), una plataforma que proporciona información sobre películas y series.

A través del archivo df_api.py se obtuvieron datos de aproximadamente 2000 películas mejor valoradas, incluyendo información como título, año de estreno, géneros, duración, sinopsis, rating y URL del poster.

Los datos recopilados fueron almacenados en el archivo peliculas_top_rated_tmdb.csv, que luego es utilizado por el sistema para generar las recomendaciones sin necesidad de realizar consultas constantes a la API.

------------------------------------------------------------------------------------------------------------------------------------------------
## Instrucciones para ejecutar el programa

1. Descargar o clonar el repositorio del proyecto.
2. Instalar las dependencias necesarias ejecutando:
```bash
pip install -r requirements.txt
```
3. Verificar que los archivos `peliculas_top_rated_tmdb.csv` e `historico_colaborativo.csv` se encuentren dentro de la carpeta `data`.
4. Ejecutar el programa principal:
```bash
python main.py
```

5. Responder el cuestionario y seguir las instrucciones que aparecen en pantalla para obtener las recomendaciones personalizadas.

------------------------------------------------------------------------------------------------------------------------------------------------
## Librerías utilizadas

El proyecto fue desarrollado en Python y utiliza las siguientes librerías:

* **Pandas**: para la manipulación y análisis de datos mediante DataFrames.
* **Requests**: para realizar consultas a la API de TMDB.
* **Matplotlib**: para la generación de gráficos y visualizaciones.
* **Pillow (PIL)**: para la carga y visualización de posters de películas.
* **CSV**: para el almacenamiento y lectura del historial colaborativo.
* **OS**: para la verificación y gestión de archivos utilizados por el sistema.

------------------------------------------------------------------------------------------------------------------------------------------------
## Estructura del repositorio

El proyecto se encuentra organizado de la siguiente manera:

### Archivo principal
* main.py: punto de entrada del sistema y coordinación general de la ejecución.

### Carpeta `src/`
* cuestionario.py: contiene el cuestionario emocional y la inferencia del perfil del usuario.
* recomendador.py: realiza el filtrado de películas y el cálculo de compatibilidad.
* colaborativo.py: gestiona el historial de elecciones y las recomendaciones colaborativas.
* graficos.py: genera los gráficos y visualizaciones del sistema.
* df_api.py: obtiene los datos desde la API de TMDB y genera el dataset.

### Carpeta `data/`
* peliculas_top_rated_tmdb.csv: dataset principal utilizado para las recomendaciones.
* historico_colaborativo.csv: archivo donde se almacenan las elecciones realizadas por los usuarios.

### Archivos adicionales
* requirements.txt: contiene las dependencias necesarias para ejecutar el proyecto.
* README.md: documentación general del trabajo.

------------------------------------------------------------------------------------------------------------------------------------------------
## Resultados y salidas

Entre las principales salidas del programa se encuentran:
* Ranking personalizado de películas recomendadas.
* Porcentaje de compatibilidad para cada película.
* Gráfico de compatibilidad entre las películas recomendadas.
* Gráfico de géneros más frecuentes dentro de las coincidencias encontradas.
* Gráfico de distribución de coincidencias por década.
* Recomendaciones colaborativas basadas en usuarios con perfiles similares.
* Registro de elecciones en el archivo historico_colaborativo.csv.

------------------------------------------------------------------------------------------------------------------------------------------------
## Diagramas de diseño

Se realizó un diagrama de flujo para representar el funcionamiento general del sistema y la interacción entre sus principales módulos.
El diagrama se encuentra adjunto en el repositorio como: diagrama_flujo.png.

------------------------------------------------------------------------------------------------------------------------------------------------
## Uso de Inteligencia Artificial

Durante el desarrollo del proyecto se utilizó ChatGPT como herramienta de apoyo para comprender el funcionamiento de la API de TMDB, organizar el código, mejorar funcionalidades y redactar documentación.

Algunos de los prompts más relevantes utilizados fueron:

* "Generá un código para visualizar qué información recibimos de la API."
* "A partir de los datos obtenidos de la API, generá un DataFrame. Tiene que acotarse a 2000 películas y deben ser las más populares. El DataFrame debe contener las columnas: título, título original, año, géneros, duración, sinopsis, rating y URL del poster."
* "Necesito que CineMood además devuelva la sinopsis de cada película que recomienda."
* "Como hago para que en los gráficos aparezca el poster de cada película y que genere un gráfico adicional que rankee las películas recomendadas por rating."
* Consultas para ajustar gráficos, corregir errores y organizar el proyecto en módulos en github.

Todo el código fue revisado, comprendido y adaptado por los integrantes del grupo.

------------------------------------------------------------------------------------------------------------------------------------------------
## Notas adicionales

* El programa utiliza los archivos `peliculas_top_rated_tmdb.csv` e `historico_colaborativo.csv`, que deben encontrarse dentro de la carpeta `data`.
* No es necesario realizar consultas a la API de TMDB para utilizar el sistema, ya que el dataset principal se encuentra previamente generado.
* En caso de querer generar nuevamente el dataset, puede ejecutarse el archivo `df_api.py`.
* Se recomienda instalar previamente todas las dependencias incluidas en `requirements.txt`.
