# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 14:22:10 2026

@author: malen
"""

import requests
import pandas as pd
import time

API_KEY = "f2ff1c095c2e59115ebca11f73907da7"
BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"


pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", 500)


def pedir_datos(endpoint, params=None):
    if params is None:
        params = {}

    params["api_key"] = API_KEY
    params["language"] = "es-ES"

    respuesta = requests.get(BASE_URL + endpoint, params=params)

    if respuesta.status_code != 200:
        raise Exception(f"Error en la API: {respuesta.status_code}")

    return respuesta.json()


def obtener_ids_top_rated(cantidad=2000):
    ids = []
    pagina = 1

    while len(ids) < cantidad:
        datos = pedir_datos(
            "/movie/top_rated",
            {"page": pagina}
        )

        for pelicula in datos["results"]:
            ids.append(pelicula["id"])

            if len(ids) >= cantidad:
                break

        pagina += 1

    return ids


def obtener_detalle_pelicula(movie_id):
    datos = pedir_datos(f"/movie/{movie_id}")

    generos = []

    for genero in datos.get("genres", []):
        generos.append(genero["name"])

    fecha = datos.get("release_date", "")
    anio = fecha[:4] if fecha else "Desconocido"

    poster_path = datos.get("poster_path")

    if poster_path:
        poster = POSTER_BASE_URL + poster_path
    else:
        poster = "Sin poster disponible"

    return {
        "titulo": datos.get("title"),
        "titulo_original": datos.get("original_title"),
        "anio": anio,
        "generos": ", ".join(generos),
        "duracion": datos.get("runtime"),
        "sinopsis": datos.get("overview"),
        "rating": datos.get("vote_average"),
        "poster": poster
    }


def crear_dataframe_top_rated(cantidad=2000):
    ids = obtener_ids_top_rated(cantidad)
    peliculas = []

    for i, movie_id in enumerate(ids, start=1):
        try:
            detalle = obtener_detalle_pelicula(movie_id)
            peliculas.append(detalle)

            print(f"{i}/{cantidad} - {detalle['titulo']}")

            time.sleep(0.05)

        except Exception as error:
            print(f"Error con ID {movie_id}: {error}")

    df = pd.DataFrame(peliculas)

    return df


def main():
    print("Descargando películas mejor rankeadas...")

    df = crear_dataframe_top_rated(2000)

    df.to_csv(
        "peliculas_top_rated_tmdb.csv",
        index=False,
        encoding="utf-8"
    )

    print("\nDataFrame creado correctamente.")
    print(f"Cantidad de filas: {len(df)}")
    print(f"Cantidad de columnas: {len(df.columns)}")

    print("\n===== PRIMERAS 20 FILAS DEL DATAFRAME =====\n")
    print(df.head(20))

    print("\nArchivo guardado como: peliculas_top_rated_tmdb.csv")
    return df

df = main()

