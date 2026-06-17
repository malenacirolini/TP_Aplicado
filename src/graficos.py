#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 16:37:25 2026

@author: sofi
"""

import pandas as pd
import matplotlib.pyplot as plt
import requests

from io import BytesIO
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox



# ──────────────────────────────────────────────────────────
# ANÁLISIS DE GÉNEROS
# ──────────────────────────────────────────────────────────

def contar_generos(df_peliculas):
    conteo = {}

    for generos in df_peliculas["generos"]:
        lista_generos = str(generos).split(",")

        for genero in lista_generos:
            genero = genero.strip()

            if genero:
                conteo[genero] = conteo.get(genero, 0) + 1

    return conteo


def mostrar_grafico_generos(df_peliculas):
    conteo = contar_generos(df_peliculas)

    if len(conteo) == 0:
        return

    generos = list(conteo.keys())
    cantidades = list(conteo.values())

    plt.figure(figsize=(10, 6))
    plt.barh(generos, cantidades)
    plt.xlabel("Cantidad de apariciones")
    plt.title("CineMood — Distribución de géneros en las coincidencias")
    plt.tight_layout()
    plt.show()


# ──────────────────────────────────────────────────────────
# VISUALIZACIÓN DEL RANKING
# ──────────────────────────────────────────────────────────

def mostrar_ranking(df_ranking):
    print("\n── Películas recomendadas para vos ──\n")

    for i, (_, fila) in enumerate(df_ranking.iterrows(), start=1):
        print(f"{i}. {fila['titulo']} ({fila['anio']})")
        print(f"   Géneros : {fila['generos']}")
        print(f"   Rating  : {fila['rating']}")
        print(f"   Match   : {fila['match']}%")
        print(f"   Sinopsis: {fila['sinopsis']}")
        print()


# ──────────────────────────────────────────────────────────
# VISUALIZACIÓN GRÁFICA DE RESULTADOS
# ──────────────────────────────────────────────────────────

def cargar_poster(url):
    try:
        if pd.isna(url) or url == "Sin poster disponible":
            return None

        respuesta = requests.get(url, timeout=5)
        imagen = Image.open(BytesIO(respuesta.content))

        return imagen

    except Exception:
        return None


def mostrar_grafico(df_ranking):
    df_plot = df_ranking.iloc[::-1].reset_index(drop=True)

    titulos = df_plot["titulo"].tolist()
    matches = df_plot["match"].tolist()
    posters = df_plot["poster"].tolist()

    fig, ax = plt.subplots(figsize=(12, 7))

    posiciones = range(len(titulos))

    ax.barh(posiciones, matches)
    ax.set_yticks(posiciones)
    ax.set_yticklabels(titulos)
    ax.set_xlabel("% de compatibilidad")
    ax.set_title("CineMood — Compatibilidad de películas recomendadas")
    ax.set_xlim(0, 115)

    for i, poster_url in enumerate(posters):
        imagen = cargar_poster(poster_url)

        if imagen is not None:
            imagebox = OffsetImage(imagen, zoom=0.06)
            ab = AnnotationBbox(
                    imagebox,
                    (matches[i] + 3, i),
                        frameon=False
)
            imagebox = OffsetImage(imagen, zoom=0.06)
            ab = AnnotationBbox(
                imagebox,
                (matches[i] + 5, i),
                frameon=False
                )
            ax.add_artist(ab)

    plt.tight_layout()
    plt.show()
    
# ──────────────────────────────────────────────────────────
# GRÁFICO DE RATINGS
# ──────────────────────────────────────────────────────────

def mostrar_grafico_rating(df_ranking):
    df_plot = df_ranking.sort_values("rating", ascending=True)

    titulos = df_plot["titulo"].tolist()
    ratings = df_plot["rating"].tolist()

    plt.figure(figsize=(10, 6))
    plt.barh(titulos, ratings)
    plt.xlabel("Rating promedio TMDB")
    plt.title("CineMood — Películas recomendadas rankeadas por rating")
    plt.xlim(0, 10)
    plt.tight_layout()
    plt.show()