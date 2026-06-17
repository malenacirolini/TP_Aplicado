# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 13:50:36 2026

@author: bausi
"""

# -*- coding: utf-8 -*-
"""
CineMood - Recomendador de películas por estado emocional
"""
import random
import requests
from io import BytesIO
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import pandas as pd
import matplotlib.pyplot as plt
import csv
import os

# ── Archivos ──────────────────────────────────────────────
ARCHIVO_PELICULAS  = "peliculas_top_rated_tmdb.csv"
ARCHIVO_HISTORIAL  = "historico_colaborativo.csv"

# ── Qué géneros corresponden a cada estado emocional ──────
ESTADOS = {
    "triste_cambiar":    ["Comedia", "Animación", "Familia"],
    "triste_acompanar":  ["Drama", "Historia", "Romance"],
    "estresado_cambiar": ["Comedia", "Acción", "Aventura"],
    "estresado_acompanar":["Suspense","Terror" "Crimen", "Drama"],
    "bien_emocionar":    ["Drama", "Ciencia ficción", "Bélica", "Acción"],
    "bien_relajar":      ["Comedia", "Fantasía", "Familia"],
    
    "reflexivo":         ["Mysterio", "Drama", "Western"],
}

# ───────────────────────────────────────────────────────────────
# PASO 1: Pedir un número válido al usuario (validación de datos)
# ───────────────────────────────────────────────────────────────
def pedir_numero(pregunta):
    while True:
        try:
            valor = int(input(pregunta))
            if 1 <= valor <= 10:
                return valor
            print("  Ingresá un número entre 1 y 10.")
        except ValueError:
            print("  Ingresá un número.")


# ──────────────────────────────────────────────────────────
# PASO 2: Hacer el cuestionario
# ──────────────────────────────────────────────────────────
def hacer_cuestionario():
    print("\n── Cuestionario (respondé del 1 al 10) ──\n")

    p1 = pedir_numero("¿Cómo te sentís? (1=muy mal, 10=muy bien): ")
    p2 = pedir_numero("¿Qué tan estresado/a estás? (1=nada, 10=muchísimo): ")
    p3 = pedir_numero("¿Querés cambiar tu estado? (1=no, quiero que me acompañe, 10=sí, quiero cambiarlo): ")
    p4 = pedir_numero("¿Qué tan involucrado/a querés estar? (1=algo liviano, 10=que me absorba): ")
    p5 = pedir_numero("¿De qué época? (1=clásicos, 10=muy reciente): ")

    return p1, p2, p3, p4, p5


# ──────────────────────────────────────────────────────────
# PASO 3: Decidir el estado emocional según las respuestas
# ──────────────────────────────────────────────────────────
def inferir_estado(p1, p2, p3, p4):
    quiere_cambiar = p3 >= 6

    if p1 <= 4:                          # se siente mal o triste
        if quiere_cambiar:
            return "triste_cambiar"
        else:
            return "triste_acompanar"

    elif p2 >= 6:                        # está estresado/ansioso
        if quiere_cambiar:
            return "estresado_cambiar"
        else:
            return "estresado_acompanar"

    elif p1 >= 7:                        # se siente bien
        if p4 >= 6:
            return "bien_emocionar"
        else:
            return "bien_relajar"

    else:                                # estado neutro
        return "reflexivo"


# ──────────────────────────────────────────────────────────
# PASO 4: Convertir P5 en un rango de años
# ──────────────────────────────────────────────────────────
def obtener_rango(p5):
    if p5 <= 3:
        return 1900, 1999, "clasico"
    elif p5 <= 6:
        return 2000, 2015, "2000-2015"
    else:
        return 2016, 2026, "reciente"


# ──────────────────────────────────────────────────────────
# PASO 5: Filtrar las películas del dataframe
# ──────────────────────────────────────────────────────────
def filtrar(df, estado, anio_desde, anio_hasta):
    generos = ESTADOS[estado]

    # Filtrar por rango de años
    df_f = df[pd.to_numeric(df["anio"], errors="coerce").between(anio_desde, anio_hasta)].copy()

    # Filtrar por género
    df_f = df_f[
        df_f["generos"].apply(
            lambda g: any(gen.lower() in str(g).lower() for gen in generos)
        )
    ].copy()

    return df_f


# ──────────────────────────────────────────────────────────
# PASO 6: Calcular el % de match de cada película
# ──────────────────────────────────────────────────────────
def calcular_match(df_f, estado):
    df_f = df_f.copy()
    generos = ESTADOS[estado]

    df_f["match"] = (df_f["rating"] / 10 * 100) * 0.8

    df_f["match"] += df_f["generos"].apply(
        lambda g: 20 if any(gen.lower() in str(g).lower() for gen in generos) else 0
    )

    df_f["match"] = df_f["match"].round(1)

    return df_f

# nuevas funciones para el nuevo grafico por genero
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


def recomendar_hasta_elegir(df_coincidencias):
    cantidad_matches = len(df_coincidencias)

    print(f"\nEncontramos {cantidad_matches} coincidencias para tu perfil.\n")

    mostrar_grafico_generos(df_coincidencias)

    if df_coincidencias.empty:
        print("No hay coincidencias para ese perfil.")
        return None

    disponibles = df_coincidencias.sample(frac=1).reset_index(drop=True)

    primeras_opciones = disponibles.head(5)
    restantes = disponibles.iloc[5:].reset_index(drop=True)

    print("\n── Primeras 5 recomendaciones ──\n")
    mostrar_ranking(primeras_opciones)
    mostrar_grafico(primeras_opciones)

    respuesta = input("¿Te interesa alguna de estas opciones? (s/n): ").strip().lower()

    if respuesta == "s":
        return pedir_eleccion(primeras_opciones)

    indice = 0

    while indice < len(restantes):
        una_peli = restantes.iloc[[indice]]

        print("\n── Nueva recomendación ──\n")
        mostrar_ranking(una_peli)

        respuesta = input("¿Te interesa esta película? (s/n): ").strip().lower()

        if respuesta == "s":
            return una_peli.iloc[0]["titulo"]

        indice += 1

    print("\nNo hay más coincidencias.")
    return None

# ──────────────────────────────────────────────────────────
# PASO 7: Mostrar el ranking en pantalla
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
# PASO 8: Mostrar el gráfico de barras
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
# ──────────────────────────────────────────────────────────
# PASO 9: Preguntar qué película eligió mirar
# ──────────────────────────────────────────────────────────
def pedir_eleccion(df_ranking):
    titulos = df_ranking["titulo"].tolist()
    print("¿Cuál vas a mirar? Ingresá el número:")
    for i, t in enumerate(titulos, start=1):
        print(f"  {i}. {t}")

    while True:
        try:
            op = int(input("\nOpción: "))
            if 1 <= op <= len(titulos):
                return titulos[op - 1]
            print(f"  Ingresá un número entre 1 y {len(titulos)}.")
        except ValueError:
            print("  Ingresá un número.")


# ──────────────────────────────────────────────────────────
# PASO 10: Guardar la elección en el historial
# ──────────────────────────────────────────────────────────
def guardar_eleccion(titulo, estado, rango):
    existe = os.path.exists(ARCHIVO_HISTORIAL)
    with open(ARCHIVO_HISTORIAL, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["estado", "rango", "titulo"])
        if not existe:
            writer.writeheader()
        writer.writerow({"estado": estado, "rango": rango, "titulo": titulo})
    print(f"\n  '{titulo}' guardada en el historial.")


# ──────────────────────────────────────────────────────────
# PASO 11: Mostrar qué eligieron usuarios con el mismo mood
# ──────────────────────────────────────────────────────────
def mostrar_colaborativo(estado, rango):
    if not os.path.exists(ARCHIVO_HISTORIAL):
        return

    df_hist = pd.read_csv(ARCHIVO_HISTORIAL)
    mismo_perfil = df_hist[(df_hist["estado"] == estado) & (df_hist["rango"] == rango)]

    if mismo_perfil.empty:
        return

    print("── Usuarios con tu mismo mood eligieron ──\n")
    for titulo in mismo_perfil["titulo"].value_counts().head(5).index:
        print(f"  • {titulo}")
    print()


# ──────────────────────────────────────────────────────────
# MAIN: une todo
# ──────────────────────────────────────────────────────────
def main():
    print("\n¡Bienvenida/o a CineMood!")

    # Cargar el dataframe de películas
    if not os.path.exists(ARCHIVO_PELICULAS):
        print(f"No se encontró '{ARCHIVO_PELICULAS}'. Ejecutá primero df_api.py.")
        return

    df = pd.read_csv(ARCHIVO_PELICULAS)

    while True:
        # Cuestionario
        p1, p2, p3, p4, p5 = hacer_cuestionario()

        # Inferir estado y rango de años
        estado = inferir_estado(p1, p2, p3, p4)
        anio_desde, anio_hasta, rango = obtener_rango(p5)

        print("\nAnalizamos tus respuestas y encontramos estas películas para vos:\n")
        # Filtrar y rankear
        df_filtrado = filtrar(df, estado, anio_desde, anio_hasta)

        if df_filtrado.empty:
            print("  No encontramos películas para ese perfil. Probá con otros valores.")
        else:
            df_coincidencias = calcular_match(df_filtrado, estado)

            mostrar_colaborativo(estado, rango)

            elegida = recomendar_hasta_elegir(df_coincidencias)
    
            if elegida is not None:
                    guardar_eleccion(elegida, estado, rango)

        # Nueva búsqueda
        if input("\n¿Otra búsqueda? (s/n): ").strip().lower() != "s":
            print("\n¡Hasta la próxima! Que disfrutes la peli 🎬\n")
            break


main()