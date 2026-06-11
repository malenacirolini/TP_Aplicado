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

El programa realiza un cuestionario compuesto por cinco preguntas relacionadas con el estado emocional y las preferencias del usuario.

A partir de las respuestas:

1. Se infiere un estado emocional.
2. Se determina un rango temporal de películas.
3. Se filtra un dataset de aproximadamente 2000 películas obtenido desde la API de TMDB.
4. Se calcula un porcentaje de compatibilidad para cada película.
5. Se genera un ranking personalizado.
6. Se muestra un gráfico comparativo.
7. Se registra la película elegida por el usuario para futuras recomendaciones colaborativas.

------------------------------------------------------------------------------------------------------------------------------------------------
## Funcionalidades principales

* Cuestionario emocional interactivo.
* Inferencia de perfiles emocionales.
* Filtrado de películas por género y época.
* Generación de rankings personalizados.
* Visualización mediante gráficos.
* Historial colaborativo de elecciones.
* Recomendaciones basadas en usuarios con perfiles similares.

------------------------------------------------------------------------------------------------------------------------------------------------
## Fuente de datos

Los datos utilizados provienen de la API pública TMDB (The Movie Database).

El archivo `df_api.py` obtiene información de aproximadamente 2000 películas utilizando los endpoints:

* `/movie/top_rated`
* `/movie/{id}`

La información recopilada se almacena en: `peliculas_top_rated_tmdb.csv`

Cada registro contiene:
* título
* año
* géneros
* duración
* sinopsis
* rating
* URL del poster

------------------------------------------------------------------------------------------------------------------------------------------------
## Librerías utilizadas

* Python
* Requests
* Pandas
* Matplotlib
* CSV

------------------------------------------------------------------------------------------------------------------------------------------------
## Estructura del proyecto:
• main.py: archivo principal para ejecutar el programa.
• cinemood.py: contiene la lógica del cuestionario, las recomendaciones y la interacción con el usuario.
• df_api.py: se encarga de obtener los datos desde la API de TMDB y generar el dataset.
• peliculas_top_rated_tmdb.csv: archivo con las películas utilizadas por el sistema.
• requirements.txt: lista de librerías necesarias para ejecutar el proyecto.
• README.md: documentación general del trabajo.

------------------------------------------------------------------------------------------------------------------------------------------------
## Funciones principales

### df_api.py
 * `pedir_datos()`
 * `obtener_ids_top_rated()`
 * `obtener_detalle_pelicula()`
 * `crear_dataframe_top_rated()`

### cinemood.py
 * `hacer_cuestionario()`
 * `inferir_estado()`
 * `obtener_rango()`
 * `filtrar()`
 * `calcular_match()`
 * `mostrar_ranking()`
 * `mostrar_grafico()`
 * `guardar_eleccion()`
 * `mostrar_colaborativo()`

------------------------------------------------------------------------------------------------------------------------------------------------
## Resultados y salidas

El sistema genera:
* Ranking de películas recomendadas.
* Porcentaje de compatibilidad para cada película.
* Gráfico de barras horizontales.
* Historial colaborativo de usuarios.
* Registro de elecciones en archivo CSV.

------------------------------------------------------------------------------------------------------------------------------------------------
## Instrucciones de ejecución

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar el programa:
```bash
python main.py
```

3. Responder el cuestionario y seguir las instrucciones en pantalla.

------------------------------------------------------------------------------------------------------------------------------------------------
## Uso de Inteligencia Artificial

Se utilizó inteligencia artificial como herramienta de apoyo para consultas técnicas relacionadas con:

* Uso de la API TMDB.
* Manejo de Pandas.
* Estructuración de funciones.
* Depuración de errores.
* Uso de GitHub.
* Generación y revisión de documentación.

###Ejemplos de prompts utilizados:

* "¿Cómo obtener películas mejor valoradas usando la API de TMDB?"
* "¿Cómo filtrar un DataFrame por género utilizando Pandas?"
* "¿Cómo exportar un DataFrame a CSV?"
* "¿Cómo crear un gráfico de barras horizontales con Matplotlib?"
* "¿Cómo organizar un proyecto Python en módulos?"

------------------------------------------------------------------------------------------------------------------------------------------------
## Diagramas de diseño

El diagrama de flujo del sistema se encuentra adjunto en el repositorio.

------------------------------------------------------------------------------------------------------------------------------------------------
## Notas adicionales

Para ejecutar nuevamente la generación del dataset, puede utilizarse el archivo `df_api.py`.

El programa principal utiliza el archivo `peliculas_top_rated_tmdb.csv` previamente generado para evitar consultas constantes a la API durante el uso normal del sistema.
