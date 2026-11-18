
"""
Participación de colocadores — Jornada 3, Valladolid.

Fuentes:
- Acta oficial del partido 2676.
- Estadísticas Data Volley J3.

Las titularidades y los totales individuales son datos
registrados. No se atribuyen colocaciones a sets concretos
sin información adicional.
"""

JORNADA = 3
RIVAL = "Valladolid"
PARTIDO_ID = 5

TITULARES = {
    1: "Abel Marina",
    2: "Leo Portillo",
    3: "Leo Portillo",
    4: "Abel Marina",
    5: "Abel Marina",
}

COLOCACIONES = {
    "Abel Marina": {
        "total": 82,
        "perfectas": 0,
        "positivas": 48,
        "emergencia": 25,
        "negativas": 8,
        "errores": 1,
    },
    "Leo Portillo": {
        "total": 50,
        "perfectas": 1,
        "positivas": 25,
        "emergencia": 17,
        "negativas": 6,
        "errores": 1,
    },
}

def obtener_titular(numero_set):
    return TITULARES.get(numero_set)

def obtener_colocaciones(nombre):
    return COLOCACIONES.get(nombre)

def resumen_participacion():
    return {
        nombre: {
            "sets_titular": [
                numero_set
                for numero_set, titular in TITULARES.items()
                if titular == nombre
            ],
            "colocaciones": datos["total"],
        }
        for nombre, datos in COLOCACIONES.items()
    }
