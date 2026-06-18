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

# ──────────────────────────────────────────────────────────
# CUESTIONARIO DEL USUARIO: Hace las cuatro preguntas.
# ──────────────────────────────────────────────────────────
def hacer_cuestionario():
    print("\n── Cuestionario (respondé del 1 al 10) ──\n")
    #las preguntas miden el estado emocional, estres, como planea seguir, y que quiere.
    p1 = pedir_numero("¿Cómo te sentís? (1=muy mal, 10=muy bien): ")
    p2 = pedir_numero("¿Qué tan estresado/a estás? (1=nada, 10=muchísimo): ")
    p3 = pedir_numero("¿Querés cambiar tu estado? (1=no, quiero que me acompañe, 10=sí, quiero cambiarlo): ")
    p4 = pedir_numero("¿Qué tan involucrado/a querés estar? (1=algo liviano, 10=que me absorba): ")

    return p1, p2, p3, p4

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
    
