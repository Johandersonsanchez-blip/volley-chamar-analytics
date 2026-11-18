DATOS_J2 = {
    1: {"ataques": 31, "centrales": 6},
    2: {"ataques": 25, "centrales": 6},
    3: {"ataques": 21, "centrales": 6},
    4: {"ataques": 33, "centrales": 13},
}

# Distribución global del equipo durante el partido.
# No representa distribuciones individuales por colocador.
REFERENCIA_ZONAS_J2 = {
    4: 43,
    3: 28,
    2: 25,
    1: 2,
    6: 1,
    5: 1,
}


def calcular_distribucion(sets, jornada=2):
    from distribucion_ofensiva import calcular_distribucion as calcular
    return calcular(sets, jornada=jornada)
