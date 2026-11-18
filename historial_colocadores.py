import sqlite3
from datetime import datetime

from tablas_html import mostrar_tabla_html


def mostrar_historial_colocadores(jugador_id, ruta_db="volley_chamar_publica.db"):
    """Muestra el historial de colocación de un jugador."""

    with sqlite3.connect(f"file:{ruta_db}?mode=ro", uri=True) as conexion:
        registros = conexion.execute(
            """
            SELECT
                p.jornada,
                p.rival,
                p.fecha,
                p.resultado,
                ef.total_acciones,
                ef.valoracion_doble_positiva,
                ef.valoracion_positiva,
                ef.valoracion_neutra,
                ef.valoracion_negativa,
                ef.valoracion_barra,
                ef.valoracion_igual
            FROM estadisticas_fundamento ef
            JOIN partidos p ON p.id = ef.partido_id
            WHERE ef.jugador_id = ?
              AND LOWER(ef.fundamento) = 'colocación'
            ORDER BY p.fecha DESC, p.jornada DESC
            """,
            (jugador_id,),
        ).fetchall()

    filas = []

    for registro in registros:
        (
            jornada, rival, fecha, resultado, total,
            doble_positiva, positiva, neutra,
            negativa, barra, igual
        ) = registro

        total = total or 0
        doble_positiva = doble_positiva or 0
        positiva = positiva or 0

        calidad = (
            (doble_positiva + positiva) / total * 100
            if total > 0 else 0
        )

        try:
            fecha_visible = datetime.strptime(
                fecha, "%Y-%m-%d"
            ).strftime("%d/%m/%Y")
        except (ValueError, TypeError):
            fecha_visible = fecha or "-"

        filas.append({
            "Jornada": jornada,
            "Rival": rival,
            "Fecha": fecha_visible,
            "Resultado": resultado,
            "Total": total,
            "++": doble_positiva,
            "+": positiva,
            "!": neutra or 0,
            "-": negativa or 0,
            "/": barra or 0,
            "=": igual or 0,
            "Calidad positiva": f"{calidad:.1f}%".replace(".", ","),
        })

    mostrar_tabla_html(
        filas,
        ayudas={
            "Total": "Número total de colocaciones realizadas.",
            "++": "Colocaciones con valoración doble positiva.",
            "+": "Colocaciones con valoración positiva.",
            "!": "Colocaciones con valoración neutra.",
            "-": "Colocaciones con valoración negativa.",
            "/": "Colocaciones con valoración barra.",
            "=": "Colocaciones con valoración igual.",
            "Calidad positiva": (
                "Porcentaje de colocaciones valoradas como ++ o +."
            ),
        },
    )
