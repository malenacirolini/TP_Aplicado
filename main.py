#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 17:19:54 2026

@author: sofi
"""
# ──────────────────────────────────────────────────────────
# PARTE 1: imports
# ──────────────────────────────────────────────────────────

#se usa para verificar si existe el CSV.
import os
#se usa para leer el dataset.
import pandas as pd

# ──────────────────────────────────────────────────────────
# PARTE 2: Importación de módulos
# ──────────────────────────────────────────────────────────

#Trae las funciones del cuestionario.
from src.cuestionario import (hacer_cuestionario, inferir_estado)
#Trae la lógica principal de recomendación.
from src.recomendador import (filtrar, calcular_match, recomendar_hasta_elegir)
#Trae el sistema colaborativo.
from src.colaborativo import (mostrar_colaborativo, guardar_eleccion) 

# ──────────────────────────────────────────────────────────
# PARTE 3:  Ruta del CSV (evita escribir la ruta varias veces)
# ──────────────────────────────────────────────────────────

ARCHIVO_PELICULAS = "data/peliculas_top_rated_tmdb.csv"

# ──────────────────────────────────────────────────────────
# PARTE 4: MAIN, funcion principal
# ──────────────────────────────────────────────────────────

def main():
    print("\n¡Bienvenida/o a CineMood!") #saludo
   
    # Verificar existencia del CSV, sino existe termina el programa
    if not os.path.exists(ARCHIVO_PELICULAS):
        print(f"No se encontró '{ARCHIVO_PELICULAS}'.")
        return
    
    # Carga todas las películas
    df = pd.read_csv(ARCHIVO_PELICULAS)

    while True:
        
        # Obtener respuestas del usuario
        (p1, p2, p3, p4, duracion_elegida,genero_evitar) =  hacer_cuestionario()

        # Determinar perfil emocional, transforma numeros en una categoria
        estado = inferir_estado(p1, p2, p3, p4)
        
        rango = "todas_las_decadas"
        
        print("\nAnalizamos tus respuestas y encontramos estas películas para vos:\n")
 
        # recibe el dataframe y el estado emocional y filtra películas compatibles
        df_filtrado = filtrar(df, estado, duracion_elegida, genero_evitar)

        #evita recomendar peliculas si no hay compatibles
        if df_filtrado.empty:
            print("No encontramos películas para ese perfil.")
      
        else:    
            # Generar ranking de coincidencias/compatibilidad
            df_coincidencias = calcular_match(df_filtrado, estado)

            # Muestra qué eligieron otros usuarios parecidos.
            mostrar_colaborativo(estado, rango)

            # Obtener película seleccionada
            elegida = recomendar_hasta_elegir(df_coincidencias)

            # Registrar elección realizada (pelicula elegida, estado emocional) en el CSV colaborativo
            if elegida is not None:
                guardar_eleccion(elegida, estado, rango)
        
        #da la opcion de repetir el programa
        if input("\n¿Otra búsqueda? (s/n): ").strip().lower() != "s":
            print("\n¡Hasta la próxima! Que disfrutes la peli 🎬\n")
            break


if __name__ == "__main__":
    main()
