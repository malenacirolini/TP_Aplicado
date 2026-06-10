# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 13:50:36 2026

@author: bausi
"""

# -*- coding: utf-8 -*-
"""
CineMood - Recomendador de películas por estado emocional
"""

import pandas as pd
import matplotlib.pyplot as plt
import csv
import os

# ── Archivos ──────────────────────────────────────────────
ARCHIVO_PELICULAS  = "peliculas_top_rated_tmdb.csv"
ARCHIVO_HISTORIAL  = "historico_colaborativo.csv"

# ── Qué géneros corresponden a cada estado emocional ──────
ESTADOS = {
    "triste_cambiar":    ["Comedy", "Animation", "Comedia", "Animación"],
    "triste_acompanar":  ["Drama", "Romance"],
    "estresado_cambiar": ["Comedy", "Adventure", "Comedia", "Aventura"],
    "estresado_acompanar":["Thriller", "Action", "Acción"],
    "bien_emocionar":    ["Drama", "Science Fiction", "Ciencia ficción"],
    "bien_relajar":      ["Comedy", "Fantasy", "Comedia", "Fantasía"],
    "reflexivo":         ["Mystery", "Thriller", "Misterio"],
}


# ──────────────────────────────────────────────────────────
# PASO 1: Pedir un número válido al usuario
# ──────────────────────────────────────────────────────────
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
        return 2016, 2030, "reciente"


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
def calcular_match(df_f):
    df_f = df_f.copy()
    df_f["match"] = (df_f["rating"] / 10 * 100).round(1)  # simple: rating sobre 10
    return df_f.sort_values("match", ascending=False).head(10)


# ──────────────────────────────────────────────────────────
# PASO 7: Mostrar el ranking en pantalla
# ──────────────────────────────────────────────────────────
def mostrar_ranking(df_ranking):
    print("\n── Películas recomendadas para vos ──\n")
    for i, (_, fila) in enumerate(df_ranking.iterrows(), start=1):
        print(f"{i}. {fila['titulo']} ({fila['anio']})")
        print(f"   Géneros : {fila['generos']}")
        print(f"   Match   : {fila['match']}%")
        print()


# ──────────────────────────────────────────────────────────
# PASO 8: Mostrar el gráfico de barras
# ──────────────────────────────────────────────────────────
def mostrar_grafico(df_ranking):
    titulos = df_ranking["titulo"].tolist()[::-1]
    matches = df_ranking["match"].tolist()[::-1]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(titulos, matches, color="#2E4DA0")
    ax.set_xlabel("% de compatibilidad")
    ax.set_title("CineMood — Compatibilidad de películas recomendadas")
    ax.set_xlim(0, 105)
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

        print(f"\n  Estado inferido: {estado.replace('_', ' ')}")
        print(f"  Rango de años  : {anio_desde}–{anio_hasta}\n")

        # Filtrar y rankear
        df_filtrado = filtrar(df, estado, anio_desde, anio_hasta)

        if df_filtrado.empty:
            print("  No encontramos películas para ese perfil. Probá con otros valores.")
        else:
            df_ranking = calcular_match(df_filtrado)

            mostrar_colaborativo(estado, rango)
            mostrar_ranking(df_ranking)
            mostrar_grafico(df_ranking)

            elegida = pedir_eleccion(df_ranking)
            guardar_eleccion(elegida, estado, rango)

        # Nueva búsqueda
        if input("\n¿Otra búsqueda? (s/n): ").strip().lower() != "s":
            print("\n¡Hasta la próxima! Que disfrutes la peli 🎬\n")
            break


main()