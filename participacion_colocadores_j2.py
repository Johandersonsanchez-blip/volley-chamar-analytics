"""
Volley Chamar Analytics
Jornada 2 - Covadonga

Reconstrucción de participación de colocadores.

Fuentes previstas:
- Acta oficial
- Informes Data Volley

No se asignan porcentajes arbitrarios.
"""

from datos_distribucion_j2 import DATOS_J2


COLOCADORES = (
    "Abel Marina",
    "Leo Portillo",
)


def crear_estructura_participacion():

    resultado = {}

    for numero_set, datos in sorted(DATOS_J2.items()):

        resultado[numero_set] = {
            "ataques_equipo": datos["ataques"],
            "ataques_centrales": datos["centrales"],
            "colocadores": {},
        }

        for colocador in COLOCADORES:

            resultado[numero_set]["colocadores"][colocador] = {
                "titular": None,
                "sustituciones": [],
                "participacion_estimada": None,
                "ataques_asociados": None,
                "distribucion": None,
                "verificado": False,
            }

    return resultado


if __name__ == "__main__":

    participacion = crear_estructura_participacion()

    for numero_set, datos in participacion.items():

        print(f"\nSET {numero_set}")
        print("Ataques del equipo:", datos["ataques_equipo"])
        print("Ataques centrales:", datos["ataques_centrales"])

        for nombre, informacion in datos["colocadores"].items():

            print(
                f"  {nombre}: "
                f"participación pendiente de verificar"
            )

    print("\nEstructura creada correctamente.")
