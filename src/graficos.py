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

    conteo_ordenado = dict(
        sorted(conteo.items(), key=lambda item: item[1], reverse=True)
    )

    generos = list(conteo_ordenado.keys())
    cantidades = list(conteo_ordenado.values())

    generos = generos[::-1]
    cantidades = cantidades[::-1]

    plt.figure(figsize=(10, 6))
    plt.barh(generos, cantidades)
    plt.xlabel("Cantidad de coincidencias")
    plt.title("CineMood — Géneros más presentes en tus coincidencias")

    for i, cantidad in enumerate(cantidades):
        plt.text(cantidad + 0.2, i, str(cantidad), va="center")

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
    

# grafico decadas

def mostrar_grafico_decadas(df_peliculas):
    df_plot = df_peliculas.copy()

    df_plot["anio"] = pd.to_numeric(df_plot["anio"], errors="coerce")
    df_plot = df_plot.dropna(subset=["anio"])

    df_plot["decada"] = (df_plot["anio"] // 10 * 10).astype(int).astype(str) + "s"

    conteo_decadas = df_plot["decada"].value_counts().sort_index()

    if conteo_decadas.empty:
        return

    plt.figure(figsize=(10, 6))
    plt.bar(conteo_decadas.index, conteo_decadas.values)
    plt.xlabel("Década")
    plt.ylabel("Cantidad de coincidencias")
    plt.title("CineMood — Distribución de coincidencias por década")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()