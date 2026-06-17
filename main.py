#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 17:19:54 2026

@author: sofi
"""

import os
import pandas as pd

from src.cuestionario import (
    hacer_cuestionario,
    inferir_estado,
    obtener_rango
)

from src.recomendador import (
    filtrar,
    calcular_match,
    recomendar_hasta_elegir
)

from src.colaborativo import (
    mostrar_colaborativo,
    guardar_eleccion
)

ARCHIVO_PELICULAS = "data/peliculas_top_rated_tmdb.csv"

# ──────────────────────────────────────────────────────────
# FUNCIÓN PRINCIPAL DEL SISTEMA
# ──────────────────────────────────────────────────────────

def main():
    print("\n¡Bienvenida/o a CineMood!")

    if not os.path.exists(ARCHIVO_PELICULAS):
        print(f"No se encontró '{ARCHIVO_PELICULAS}'.")
        return

    df = pd.read_csv(ARCHIVO_PELICULAS)

    while True:
        
        # Obtener respuestas del usuario
        p1, p2, p3, p4, p5 = hacer_cuestionario()

        # Determinar perfil emocional
        estado = inferir_estado(p1, p2, p3, p4)

        # Determinar rango temporal preferido
        anio_desde, anio_hasta, rango = obtener_rango(p5)

        print("\nAnalizamos tus respuestas y encontramos estas películas para vos:\n")
 
        # Filtrar películas compatibles
        df_filtrado = filtrar(df, estado, anio_desde, anio_hasta)

        if df_filtrado.empty:
            print("No encontramos películas para ese perfil.")
      
        else:    
            # Generar ranking de coincidencias
            df_coincidencias = calcular_match(df_filtrado, estado)

            # Mostrar sugerencias colaborativas
            mostrar_colaborativo(estado, rango)

            # Obtener película seleccionada
            elegida = recomendar_hasta_elegir(df_coincidencias)

            # Registrar elección realizada
            if elegida is not None:
                guardar_eleccion(elegida, estado, rango)

        if input("\n¿Otra búsqueda? (s/n): ").strip().lower() != "s":
            print("\n¡Hasta la próxima! Que disfrutes la peli 🎬\n")
            break


if __name__ == "__main__":
    main()