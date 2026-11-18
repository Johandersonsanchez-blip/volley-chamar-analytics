"""
Volley Chamar Analytics
Jornada 2 — Covadonga

Modelo provisional de distribución individual por colocador.
Las participaciones son estimaciones configurables, no datos
confirmados del acta.
"""

from datos_distribucion_j2 import DATOS_J2, calcular_distribucion

ZONAS = (1, 2, 3, 4, 5, 6)

# Participación provisional por set.
# Cada fila debe sumar 1.0.
# Sustituiremos estos valores cuando validemos los cambios.
PARTICIPACION = {
    1: {"Abel Marina": 0.20, "Leo Portillo": 0.80},
    2: {"Abel Marina": 0.80, "Leo Portillo": 0.20},
    3: {"Abel Marina": 0.20, "Leo Portillo": 0.80},
    4: {"Abel Marina": 0.20, "Leo Portillo": 0.80},
}


def calcular_distribucion_individual_j2(colocador):
    if colocador not in ("Abel Marina", "Leo Portillo"):
        raise ValueError("Colocador no reconocido")

    acumulado = {zona: 0.0 for zona in ZONAS}
    ataques_estimados = 0.0
    detalle = {}

    for numero_set in sorted(DATOS_J2):
        datos = DATOS_J2[numero_set]
        participacion = PARTICIPACION[numero_set][colocador]

        distribucion, ataques = calcular_distribucion(
            [numero_set],
            jornada=2
        )

        ataques_asignados = ataques * participacion
        ataques_estimados += ataques_asignados

        detalle[numero_set] = {
            "participacion_estimada": participacion * 100,
            "ataques_estimados": ataques_asignados,
            "distribucion": distribucion,
        }

        for zona in ZONAS:
            acumulado[zona] += (
                distribucion.get(zona, 0)
                * ataques_asignados
                / 100
            )

    if ataques_estimados:
        porcentajes = {
            zona: round(
                acumulado[zona] / ataques_estimados * 100,
                2
            )
            for zona in ZONAS
        }
    else:
        porcentajes = {zona: 0.0 for zona in ZONAS}

    return {
        "colocador": colocador,
        "ataques_estimados": round(ataques_estimados, 1),
        "distribucion": porcentajes,
        "detalle_sets": detalle,
        "metodo": "Estimación provisional ponderada por participación",
    }


if __name__ == "__main__":
    for nombre in ("Abel Marina", "Leo Portillo"):
        resultado = calcular_distribucion_individual_j2(nombre)

        print(f"\n{nombre}")
        print("Ataques estimados:", resultado["ataques_estimados"])

        for zona, porcentaje in resultado["distribucion"].items():
            print(f"Zona {zona}: {porcentaje:.2f}%")

        print("Total:", round(sum(resultado["distribucion"].values()), 2))
