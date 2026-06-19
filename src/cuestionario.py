#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 16:36:59 2026

@author: sofi
"""

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────
# VALIDACIÓN DE ENTRADAS: Recibe una pregunta y se asegura de que el usuario escriba un número entre 1 y 10
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────

def pedir_numero(pregunta):
    while True:
        try:
            valor = int(input(pregunta))
            if 1 <= valor <= 10:
                return valor
            print("  Ingresá un número entre 1 y 10.")
        except ValueError:
            print("  Ingresá un número.")

#usamos try/except por si escribe texto, asi evitamos que se rompa si pasa esto.

def pedir_duracion():
    print("\n¿Cuánto tiempo querés dedicarle a la película?")
    print("1. Hasta 90 minutos")
    print("2. Entre 91 y 120 minutos")
    print("3. Más de 120 minutos")
    print("4. Me da igual")

    while True:
        try:
            opcion = int(input("\nOpción: "))

            if opcion in [1, 2, 3, 4]:
                return opcion

            print("Ingresá una opción entre 1 y 4.")

        except ValueError:
            print("Ingresá un número.")

GENEROS_DISPONIBLES = [
    "Acción",
    "Animación",
    "Aventura",
    "Bélica",
    "Ciencia ficción",
    "Comedia",
    "Crimen",
    "Drama",
    "Familia",
    "Fantasía",
    "Historia",
    "Misterio",
    "Romance",
    "Suspense",
    "Terror",
    "Western"
]


def pedir_genero_evitar():
    print("\n¿Hay algún género que no quieras ver?")

    for numero, genero in enumerate(GENEROS_DISPONIBLES, start=1):
        print(f"{numero}. {genero}")

    opcion_ninguno = len(GENEROS_DISPONIBLES) + 1
    print(f"{opcion_ninguno}. Ninguno")

    while True:
        try:
            opcion = int(input("\nOpción: "))

            if 1 <= opcion <= len(GENEROS_DISPONIBLES):
                return GENEROS_DISPONIBLES[opcion - 1]

            if opcion == opcion_ninguno:
                return None

            print(
                f"Ingresá una opción entre 1 y {opcion_ninguno}."
            )

        except ValueError:
            print("Ingresá un número.")

# ──────────────────────────────────────────────────────────
# CUESTIONARIO DEL USUARIO: Hace las cuatro preguntas.
# ──────────────────────────────────────────────────────────
def hacer_cuestionario():
    print("\n── Cuestionario ──\n")

    p1 = pedir_numero(
        "¿Cómo te sentís? (1=muy mal, 10=muy bien): "
    )

    p2 = pedir_numero(
        "¿Qué tan estresado/a estás? "
        "(1=nada, 10=muchísimo): "
    )

    p3 = pedir_numero(
        "¿Querés cambiar tu estado? "
        "(1=no, quiero que me acompañe, "
        "10=sí, quiero cambiarlo): "
    )

    p4 = pedir_numero(
        "¿Qué tan involucrado/a querés estar? "
        "(1=algo liviano, 10=que me absorba): "
    )

    duracion_elegida = pedir_duracion()
    genero_evitar = pedir_genero_evitar()

    return (
        p1,
        p2,
        p3,
        p4,
        duracion_elegida,
        genero_evitar
    )

# ──────────────────────────────────────────────────────────────
# ANÁLISIS DEL PERFIL EMOCIONAL: transforma en perfil emocional
# ──────────────────────────────────────────────────────────────
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
    
