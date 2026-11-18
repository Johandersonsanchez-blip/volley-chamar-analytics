"""J3 Valladolid: volúmenes oficiales y atribución por set ESTIMADA.
No atribuye asistencias individuales ni porcentajes por zona como hechos.
"""
from participacion_colocadores_j3 import TITULARES, COLOCACIONES

# Acciones ofensivas por set registradas en sets_partido; suman 139,
# distintas de las 156 acciones de ataque del informe global.
ATAQUES_SET = {1: 42, 2: 17, 3: 31, 4: 33, 5: 16}
NOMBRES = tuple(COLOCACIONES)

def estimar_volumen_por_set():
    """Ajuste proporcional a titularidades, calibrado a 82/50 colocaciones.

    El reparto de 85/15 es una HIPÓTESIS, no dato de acta.
    El ajuste conserva exactamente los totales oficiales de cada colocador.
    """
    total = sum(ATAQUES_SET.values())
    # Estimación de oportunidades: ponderación por ataques de cada set.
    pesos = {s: {n: ATAQUES_SET[s] * (0.85 if TITULARES[s] == n else 0.15)
                 for n in NOMBRES} for s in ATAQUES_SET}
    # Calibración por columna; no se fuerza suma por fila porque las
    # colocaciones (132) y los ataques por set (139) no son equivalentes.
    for n in NOMBRES:
        factor = COLOCACIONES[n]['total'] / sum(pesos[s][n] for s in pesos)
        for s in pesos:
            pesos[s][n] *= factor
    return pesos

def obtener_resumen(nombre, sets):
    if nombre not in COLOCACIONES:
        return None
    sets = list(sets)
    if not sets or any(s not in ATAQUES_SET for s in sets):
        raise ValueError('Set no registrado en J3')
    estimados = estimar_volumen_por_set()
    return {
        'nombre': nombre,
        'titulares': [s for s in sets if TITULARES[s] == nombre],
        'colocaciones_oficiales_partido': COLOCACIONES[nombre],
        'colocaciones_estimadas_seleccion': sum(estimados[s][nombre] for s in sets),
        'estimacion_por_set': {s: round(estimados[s][nombre], 1) for s in sets},
        'ataques_equipo_seleccion': sum(ATAQUES_SET[s] for s in sets),
        'metodo': 'Estimación por volumen ofensivo y titularidad (hipótesis 85/15), calibrada al total oficial de colocaciones.',
    }
