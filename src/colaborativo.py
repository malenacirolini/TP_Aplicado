#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 16:38:04 2026

@author: sofi
"""

import pandas as pd
import csv
import os

ARCHIVO_HISTORIAL = "data/historico_colaborativo.csv"

# ──────────────────────────────────────────────────────────
# REGISTRO DE ELECCIONES DEL USUARIO
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
# RECOMENDACIÓN COLABORATIVA
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

