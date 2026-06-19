#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 16:37:41 2026

@author: sofi
"""

import pandas as pd
from src.graficos import (
    mostrar_ranking,
    mostrar_grafico,
    mostrar_grafico_generos,
    mostrar_grafico_decadas
)
#Cuando queremos que muestre gráficos o rankings lo delega a gráficos.py

# ──────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PERFILES EMOCIONALES
# ──────────────────────────────────────────────────────────

ESTADOS = {
    "triste_cambiar":    ["Comedia", "Animación", "Familia"],
    "triste_acompanar":  ["Drama", "Historia", "Romance"],
    "estresado_cambiar": ["Comedia", "Acción", "Aventura"],
    "estresado_acompanar":["Suspense","Terror", "Crimen", "Drama"],
    "bien_emocionar":    ["Drama", "Ciencia ficción", "Bélica", "Acción"],
    "bien_relajar":      ["Comedia", "Fantasía", "Familia"],
    "reflexivo":         ["Mysterio", "Drama", "Western"],
}

# ──────────────────────────────────────────────────────────
# FILTRADO DE PELÍCULAS
# ──────────────────────────────────────────────────────────0]
def filtrar(df, estado, duracion_elegida, genero_evitar):
    generos_estado = ESTADOS[estado]

    df_f = df.copy()

    df_f["duracion"] = pd.to_numeric(
        df_f["duracion"],
        errors="coerce"
    )

    df_f = df_f.dropna(subset=["duracion"])

    # Filtrar por géneros compatibles con el perfil.
    df_f = df_f[
        df_f["generos"].apply(
            lambda generos_pelicula: any(
                genero.lower() in str(generos_pelicula).lower()
                for genero in generos_estado
            )
        )
    ].copy()

    # Filtrar por duración.
    if duracion_elegida == 1:
        df_f = df_f[df_f["duracion"] <= 90]

    elif duracion_elegida == 2:
        df_f = df_f[
            df_f["duracion"].between(91, 120)
        ]

    elif duracion_elegida == 3:
        df_f = df_f[df_f["duracion"] > 120]

    # Excluir el género que no quiere ver.
    if genero_evitar is not None:
        df_f = df_f[
            ~df_f["generos"].str.contains(
                genero_evitar,
                case=False,
                na=False,
                regex=False
            )
        ].copy()

    return df_f
# ──────────────────────────────────────────────────────────
# CÁLCULO DEL PORCENTAJE DE COMPATIBILIDAD
# ──────────────────────────────────────────────────────────

def calcular_match(df_f, estado):    # Recibe las películas filtradas
    df_f = df_f.copy()               # Hace una copia para no modificar el df original
    generos = ESTADOS[estado]

    df_f["match"] = (df_f["rating"] / 10 * 100) * 0.8

    df_f["match"] += df_f["generos"].apply(
        lambda g: 20 if any(gen.lower() in str(g).lower() for gen in generos) else 0
    )

    df_f["match"] = df_f["match"].round(1)

    return df_f


# ──────────────────────────────────────────────────────────
# PROCESO DE RECOMENDACIÓN
# ──────────────────────────────────────────────────────────

def pedir_si_no(pregunta):    # Valida, solo acepta s o n
    while True:
        respuesta = input(pregunta).strip().lower()

        if respuesta in ["s", "n"]:
            return respuesta

        print("  Ingresá 's' para sí o 'n' para no.")


def recomendar_hasta_elegir(df_coincidencias):
    cantidad_matches = len(df_coincidencias)  # Cuenta cuantas peliculas encontro

    print(f"\nEncontramos {cantidad_matches} coincidencias para tu perfil.\n")

    if df_coincidencias.empty:
        print("No hay coincidencias para ese perfil.")
        return None

    mostrar_grafico_generos(df_coincidencias)
    mostrar_grafico_decadas(df_coincidencias)
    
    disponibles = df_coincidencias.sample(frac=1).reset_index(drop=True) #mezcla las filas

    primeras_opciones = disponibles.head(5)    # Toma las primeras 5 recomendaciones
    restantes = disponibles.iloc[5:].reset_index(drop=True) # Guarda las demas

    print("\n── Primeras 5 recomendaciones ──\n")
    mostrar_ranking(primeras_opciones)
    mostrar_grafico(primeras_opciones)

    respuesta = pedir_si_no("¿Te interesa alguna de estas opciones? (s/n): ")

    if respuesta == "s":
        return pedir_eleccion(primeras_opciones)

    indice = 0

    while indice < len(restantes):
        quiere_otra = pedir_si_no("\n¿Querés que te tire otra coincidencia? (s/n): ")

        if quiere_otra == "n":
            print("\nBúsqueda finalizada.")
            return None

        una_peli = restantes.iloc[[indice]]

        print("\n── Nueva recomendación ──\n")
        mostrar_ranking(una_peli)

        respuesta = pedir_si_no("¿Te interesa esta película? (s/n): ")

        if respuesta == "s":
            return una_peli.iloc[0]["titulo"]

        indice += 1

    print("\nNo hay más coincidencias.")
    return None

# ──────────────────────────────────────────────────────────
#  SELECCIÓN DE PELÍCULA
# ──────────────────────────────────────────────────────────

def pedir_eleccion(df_ranking):    # Recibe las 5 peliculas
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

