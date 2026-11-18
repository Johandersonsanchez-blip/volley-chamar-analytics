from distribucion_individual_j2 import calcular_distribucion_individual_j2
import streamlit as st
import plotly.graph_objects as go


# Datos de la jornada 1: Las Rozas.
# Ataques registrados por Data Volley.
# Los ataques de centrales se utilizan como aproximación a zona 3.
DATOS_J1 = {
    1: {"ataques": 22, "centrales": 4, "titular": "Abel Marina"},
    2: {"ataques": 26, "centrales": 7, "titular": "Abel Marina"},
    3: {"ataques": 33, "centrales": 9, "titular": "Abel Marina"},
    4: {"ataques": 41, "centrales": 6, "titular": "Leo Portillo"},
}

# Distribución global observada en Data Volley.
# Porcentajes redondeados en el informe.
REFERENCIA_ZONAS = {
    4: 48,
    3: 21,
    2: 25,
    5: 0,
    6: 2,
    1: 3,
}



# ============================================================
# JORNADA 2 — COVADONGA
# Datos colectivos procedentes de Data Volley.
# ============================================================

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


# INTEGRACION_J4_PALENCIA_V1
# J4 — CYL Palencia 2028
# Fuente: Data Volley, 25/10/2026.
# Los ataques de centrales corresponden a Caamaño y Cancino.

DATOS_J4 = {
    1: {"ataques": 36, "centrales": 6},
    2: {"ataques": 30, "centrales": 5},
    3: {"ataques": 32, "centrales": 7},
    4: {"ataques": 32, "centrales": 8},
    5: {"ataques": 13, "centrales": 2},
}


# INTEGRACION_J5_ACENVOLLEY
# Jornada 5 — Acenvolley.
# Ataques oficiales por set según Data Volley.
# Los ataques de centrales permiten estimar zona 3.

DATOS_J5 = {
    1: {"ataques": 34, "centrales": 8},
    2: {"ataques": 34, "centrales": 8},
    3: {"ataques": 26, "centrales": 8},
    4: {"ataques": 28, "centrales": 6},
}

# Estadísticas oficiales individuales del partido.
# No representan colocaciones desglosadas por set.
COLOCACIONES_J5 = {
    "Abel Marina": {
        "total": 54,
        "perfectas": 1,
        "positivas": 27,
    },
    "Leo Portillo": {
        "total": 50,
        "perfectas": 0,
        "positivas": 31,
    },
}

COLOCACIONES_J4 = {
    "Abel Marina": {
        "total": 101,
        "perfectas": 1,
        "positivas": 76,
        "saques": 11,
        "errores_saque": 0,
        "defensas": 6,
        "ataques": 5,
        "puntos": 2,
    },
    "Leo Portillo": {
        "total": 13,
        "perfectas": 0,
        "positivas": 11,
        "saques": 2,
        "errores_saque": 1,
        "defensas": 2,
        "ataques": 0,
        "puntos": 0,
    },
}

def calcular_distribucion(sets, jornada=1):
    """
    Calcula la distribución ofensiva del equipo.

    J1: estimación basada en ataques de centrales.
    J2: distribución global observada en Data Volley.
    """

    # CHV_J7_DISTRIBUCION_COLECTIVA_V2
    # Datos oficiales J7 - CV Oleiros (Data Volley).
    # Formato: set: (ataques totales, ataques centrales).
    if jornada == 7:
        datos_j7 = {
            1: (28, 9),
            2: (35, 10),
            3: (33, 5),
            4: (28, 9),
        }

        if not sets or any(s not in datos_j7 for s in sets):
            return {}, 0

        ataques = sum(datos_j7[s][0] for s in sets)
        centrales = sum(datos_j7[s][1] for s in sets)

        if ataques == 0:
            return {}, 0

        proporcion_central = centrales / ataques
        zonas_exteriores = [4, 2, 5, 6, 1]

        peso_total = sum(
            REFERENCIA_ZONAS_J2[z]
            for z in zonas_exteriores
        )

        distribucion = {
            3: proporcion_central * 100
        }

        for zona in zonas_exteriores:
            distribucion[zona] = (
                (1 - proporcion_central)
                * REFERENCIA_ZONAS_J2[zona]
                / peso_total
                * 100
            )

        return distribucion, ataques

    if jornada == 2:
        ataques = sum(DATOS_J2[s]["ataques"] for s in sets)

        if sorted(sets) == [1, 2, 3, 4]:
            return REFERENCIA_ZONAS_J2.copy(), ataques

        # Distribución estimada por set siguiendo el modelo de J1.
        centrales = sum(DATOS_J2[s]["centrales"] for s in sets)

        if ataques == 0:
            return {}, 0

        proporcion_central = centrales / ataques

        zonas_exteriores = [4, 2, 5, 6, 1]

        peso_total = sum(
            REFERENCIA_ZONAS_J2[z] for z in zonas_exteriores
        )

        distribucion = {3: proporcion_central * 100}

        for zona in zonas_exteriores:
            distribucion[zona] = (
                (1 - proporcion_central)
                * REFERENCIA_ZONAS_J2[zona]
                / peso_total
                * 100
            )

        return distribucion, ataques




    if jornada == 5:
        if not sets or any(s not in DATOS_J5 for s in sets):
            raise ValueError("Set no disponible en Acenvolley J5")

        ataques = sum(DATOS_J5[s]["ataques"] for s in sets)
        centrales = sum(DATOS_J5[s]["centrales"] for s in sets)

        if ataques == 0:
            return {}, 0

        proporcion_central = centrales / ataques
        zonas_exteriores = [4, 2, 5, 6, 1]

        peso_total = sum(
            REFERENCIA_ZONAS_J2[z]
            for z in zonas_exteriores
        )

        distribucion = {3: proporcion_central * 100}

        for zona in zonas_exteriores:
            distribucion[zona] = (
                (1 - proporcion_central)
                * REFERENCIA_ZONAS_J2[zona]
                / peso_total
                * 100
            )

        return distribucion, ataques

    if jornada == 4:
        if not sets or any(s not in DATOS_J4 for s in sets):
            raise ValueError("Set no disponible en Palencia J4")

        ataques = sum(DATOS_J4[s]["ataques"] for s in sets)
        centrales = sum(DATOS_J4[s]["centrales"] for s in sets)

        if ataques == 0:
            return {}, 0

        proporcion_central = centrales / ataques
        zonas_exteriores = [4, 2, 5, 6, 1]

        peso_total = sum(
            REFERENCIA_ZONAS_J2[z]
            for z in zonas_exteriores
        )

        distribucion = {
            3: proporcion_central * 100
        }

        for zona in zonas_exteriores:
            distribucion[zona] = (
                (1 - proporcion_central)
                * REFERENCIA_ZONAS_J2[zona]
                / peso_total
                * 100
            )

        return distribucion, ataques

    if jornada == 3:
        # Distribución colectiva estimada por set.
        # Misma metodología que J1 y J2:
        # proporción de ataques centrales y reparto
        # del resto según REFERENCIA_ZONAS_J2.

        datos_por_set = {
            1: (29, 5),
            2: (33, 7),
            3: (33, 5),
            4: (41, 11),
            5: (20, 6),
        }

        if not sets or any(s not in datos_por_set for s in sets):
            raise ValueError("Set no disponible en Valladolid J3")

        ataques = sum(datos_por_set[s][0] for s in sets)
        centrales = sum(datos_por_set[s][1] for s in sets)

        if ataques == 0:
            return {}, 0

        proporcion_central = centrales / ataques
        zonas_exteriores = [4, 2, 5, 6, 1]

        peso_total = sum(
            REFERENCIA_ZONAS_J2[zona]
            for zona in zonas_exteriores
        )

        distribucion = {
            3: proporcion_central * 100
        }

        for zona in zonas_exteriores:
            distribucion[zona] = (
                (1 - proporcion_central)
                * REFERENCIA_ZONAS_J2[zona]
                / peso_total
                * 100
            )

        return distribucion, ataques


    # J6 — Jatorkide. Distribución colectiva estimada por set.
    if jornada == 6:
        datos_j6 = {
            1: (29, 5),
            2: (33, 7),
            3: (33, 5),
            4: (41, 11),
        }

        if not sets or any(s not in datos_j6 for s in sets):
            raise ValueError("Set no disponible para J6")

        ataques = sum(datos_j6[s][0] for s in sets)
        centrales = sum(datos_j6[s][1] for s in sets)

        if ataques == 0:
            return {}, 0

        proporcion_central = centrales / ataques
        zonas_exteriores = [4, 2, 5, 6, 1]

        peso_total = sum(
            REFERENCIA_ZONAS_J2[z]
            for z in zonas_exteriores
        )

        distribucion = {
            3: proporcion_central * 100
        }

        for zona in zonas_exteriores:
            distribucion[zona] = (
                (1 - proporcion_central)
                * REFERENCIA_ZONAS_J2[zona]
                / peso_total
                * 100
            )

        return distribucion, ataques

    if jornada != 1:
        raise ValueError("Jornada no disponible")

    ataques = sum(DATOS_J1[s]["ataques"] for s in sets)
    centrales = sum(DATOS_J1[s]["centrales"] for s in sets)

    if ataques == 0:
        return {}, 0

    proporcion_central = centrales / ataques

    zonas_exteriores = [4, 2, 5, 6, 1]
    peso_total = sum(
        REFERENCIA_ZONAS[z] for z in zonas_exteriores
    )

    distribucion = {3: proporcion_central * 100}

    for zona in zonas_exteriores:
        distribucion[zona] = (
            (1 - proporcion_central)
            * REFERENCIA_ZONAS[zona]
            / peso_total
            * 100
        )

    return distribucion, ataques



def crear_cancha(distribucion):
    """Cancha de voleibol con red y estilo cinematográfico."""
    import plotly.graph_objects as go

    figura = go.Figure()

    posiciones = {
        4: (0, 1), 3: (1, 1), 2: (2, 1),
        5: (0, 0), 6: (1, 0), 1: (2, 0),
    }

    # Fondo y zonas con iluminación proporcional.
    for zona, (x, y) in posiciones.items():
        porcentaje = distribucion.get(zona)
        intensidad = min(porcentaje / 55, 1) if porcentaje is not None else 0

        figura.add_shape(
            type="rect",
            x0=x, y0=y, x1=x+1, y1=y+1,
            line=dict(color="#D9AD25", width=2),
            fillcolor=f"rgba(255, 200, 0, {0.10 + intensidad * 0.75:.3f})",
            layer="below",
        )

        figura.add_annotation(
            x=x+0.5,
            y=y+0.5,
            text=(
                f"<b>ZONA {zona}</b><br>"
                f"<span style='font-size:25px'>"
                f"{porcentaje:.1f}%</span>" if porcentaje is not None else "<span style='font-size:17px'>Sin datos</span>"
            ),
            showarrow=False,
            font=dict(color="#FFFFFF", size=13),
            align="center",
        )

    # Línea de ataque.
    figura.add_shape(
        type="line",
        x0=0, y0=1, x1=3, y1=1,
        line=dict(color="#FFFFFF", width=3),
    )

    # Red de voleibol sobre la parte superior de la cancha.
    for x in [i / 15 for i in range(46)]:
        figura.add_shape(
            type="line",
            x0=x, y0=1.92, x1=x, y1=2.12,
            line=dict(color="rgba(255,255,255,0.45)", width=1),
        )

    for y in [1.92, 1.97, 2.02, 2.07, 2.12]:
        figura.add_shape(
            type="line",
            x0=0, y0=y, x1=3, y1=y,
            line=dict(color="rgba(255,255,255,0.55)", width=1),
        )

    # Cinta superior y postes.
    figura.add_shape(
        type="line",
        x0=0, y0=2.12, x1=3, y1=2.12,
        line=dict(color="#FFFFFF", width=5),
    )

    for x in [-0.06, 3.06]:
        figura.add_shape(
            type="line",
            x0=x, y0=1.85, x1=x, y1=2.20,
            line=dict(color="#E9EDF2", width=5),
        )

    figura.update_layout(
        paper_bgcolor="#101218",
        plot_bgcolor="#101218",
        height=510,
        margin=dict(l=15, r=15, t=30, b=20),
        xaxis=dict(range=[-0.2, 3.2], visible=False, fixedrange=True),
        yaxis=dict(
            range=[-0.1, 2.3],
            visible=False,
            fixedrange=True,
            scaleanchor="x",
            scaleratio=1,
        ),
        showlegend=False,
    )

    return figura


def mostrar_distribucion_ofensiva(jugador_id, temporada_id):
    """Visualiza la distribución ofensiva colectiva por jornada."""

    st.markdown("### 🏐 Distribución ofensiva por zonas")

    jornada = st.selectbox(
        "Jornada",
        [
            "J1 — Las Rozas",
            "J2 — Covadonga",
            "J3 — Valladolid",
            "J4 — Palencia",
            "J5 — Acenvolley",
            "J6 — Jatorkide",
            "J7 — CV Oleiros",
        ],
        key=f"distribucion_jornada_{jugador_id}_{temporada_id}",
    )

    numero_jornada = int(jornada[1])

    total_sets = 5 if numero_jornada in (3, 4) else 4

    opciones = ["Partido completo"] + [
        f"Set {numero}" for numero in range(1, total_sets + 1)
    ]

    seleccion = st.selectbox(
        "Set",
        opciones,
        key=f"distribucion_set_{jugador_id}_{temporada_id}",
    )

    if seleccion == "Partido completo":
        sets = list(range(1, total_sets + 1))
    else:
        sets = [int(seleccion.split()[-1])]





    # INTEGRACION_J6_JATORKIDE_V1
    # Estadísticas oficiales almacenadas en SQLite.
    # La distribución ofensiva por zonas se incorporará
    # cuando exista un desglose suficiente por set.

    # CHV_J7_TARJETAS_RENDIMIENTO
    if numero_jornada == 7:
        import sqlite3

        with sqlite3.connect(
            "file:volley_chamar_publica.db?mode=ro",
            uri=True
        ) as conexion:
            jugador = conexion.execute(
                "SELECT nombre FROM jugadores WHERE id = ?",
                (jugador_id,)
            ).fetchone()

        nombre = jugador[0].lower() if jugador else ""

        if "portillo" in nombre:
            colocaciones = 72
            positivas = 52
        elif "marina" in nombre:
            colocaciones = 31
            positivas = 14
        else:
            colocaciones = None
            positivas = None

        if colocaciones is not None:
            calidad = positivas / colocaciones * 100

            st.markdown("### 🏐 Rendimiento del colocador")

            columnas = st.columns(3)

            tarjetas = [
                (
                    "🏐 COLOCACIONES OFICIALES",
                    str(colocaciones),
                    "Total de J7"
                ),
                (
                    "🎯 CALIDAD POSITIVA",
                    f"{calidad:.1f}%",
                    "Calidad oficial de J7"
                ),
                (
                    "📊 COLOCACIONES POSITIVAS",
                    str(positivas),
                    "Perfectas + positivas"
                ),
            ]

            for columna, (titulo, valor, descripcion) in zip(
                columnas, tarjetas
            ):
                with columna:
                    st.markdown(
                        f"""
                        <div style="
                            background:linear-gradient(
                                135deg,#24252d,#15161c
                            );
                            border:1px solid #41434d;
                            border-top:4px solid #ffd700;
                            border-radius:17px;
                            padding:25px 12px;
                            text-align:center;
                            min-height:175px;
                        ">
                            <div style="
                                color:#d6d6df;
                                font-size:13px;
                                font-weight:800;
                            ">{titulo}</div>
                            <div style="
                                color:white;
                                font-size:39px;
                                font-weight:800;
                                margin:22px 0;
                            ">{valor}</div>
                            <div style="
                                color:#a9a9b5;
                                font-size:12px;
                            ">{descripcion}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    # CHV_VISUAL_J7_OLEIROS
    if numero_jornada == 7:
        st.markdown("#### Jornada 7 · CV Oleiros")


        # CHV_J7_COMPLEMENTOS_V2
        # Estadísticas oficiales y participación estimada.
        import sqlite3

        with sqlite3.connect(
            "file:volley_chamar_publica.db?mode=ro",
            uri=True
        ) as conexion_j7:
            fila = conexion_j7.execute(
                "SELECT nombre FROM jugadores WHERE id = ?",
                (jugador_id,)
            ).fetchone()

        nombre_j7 = fila[0].lower() if fila else ""

        datos_j7 = None

        if "portillo" in nombre_j7:
            datos_j7 = {
                "colocaciones": 72,
                "saques": 21,
                "errores_saque": 2,
                "ataques": 2,
                "puntos": 1,
                "titular": True,
            }
        elif "marina" in nombre_j7:
            datos_j7 = {
                "colocaciones": 31,
                "saques": 6,
                "errores_saque": 0,
                "ataques": 0,
                "puntos": 0,
                "titular": False,
            }

        if datos_j7:
            st.markdown("### 📊 Otras estadísticas de la jornada")

            columnas = st.columns(4)

            tarjetas = [
                ("🎾 SAQUES", datos_j7["saques"]),
                ("❌ ERRORES DE SAQUE", datos_j7["errores_saque"]),
                ("⚡ ATAQUES", datos_j7["ataques"]),
                ("🏆 PUNTOS", datos_j7["puntos"]),
            ]

            for columna, (titulo, valor) in zip(columnas, tarjetas):
                with columna:
                    st.markdown(
                        f"""
                        <div style="
                            background:linear-gradient(135deg,#24252d,#15161c);
                            border:1px solid #41434d;
                            border-top:4px solid #ffd700;
                            border-radius:16px;
                            padding:22px 10px;
                            text-align:center;
                            min-height:140px;
                        ">
                            <div style="
                                color:#d6d6df;
                                font-size:13px;
                                font-weight:800;
                            ">{titulo}</div>
                            <div style="
                                color:white;
                                font-size:35px;
                                font-weight:800;
                                margin-top:20px;
                            ">{valor}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            st.markdown("### Participación estimada por set")

            ataques_sets = [28, 35, 33, 28]
            total_ataques = sum(ataques_sets)
            total_colocaciones = datos_j7["colocaciones"]

            columnas_sets = st.columns(4)

            for numero_set, (columna, ataques_set) in enumerate(
                zip(columnas_sets, ataques_sets),
                start=1
            ):
                estimacion = (
                    total_colocaciones * ataques_set / total_ataques
                )

                estado = (
                    "TITULAR" if datos_j7["titular"] else "NO TITULAR"
                )

                with columna:
                    st.markdown(
                        f"""
                        <div style="
                            background:linear-gradient(135deg,#24252d,#15161c);
                            border:1px solid #41434d;
                            border-top:4px solid #ffd700;
                            border-radius:16px;
                            padding:22px 10px;
                            text-align:center;
                            min-height:160px;
                        ">
                            <div style="
                                color:#d6d6df;
                                font-size:14px;
                                font-weight:800;
                            ">SET {numero_set}</div>
                            <div style="
                                color:white;
                                font-size:35px;
                                font-weight:800;
                                margin:20px 0;
                            ">{estimacion:.1f}</div>
                            <div style="
                                color:#ffd700;
                                font-size:12px;
                                font-weight:800;
                            ">{estado}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            st.caption(
                "Participación estimada proporcional al volumen "
                "de ataques por set; no son colocaciones "
                "individuales registradas."
            )

        st.markdown("##### Distribución ofensiva por zonas")

        distribucion, ataques = calcular_distribucion(
            sets,
            jornada=7
        )

        st.metric("Ataques analizados", ataques)

        st.caption(
            "J7 — Distribución ofensiva colectiva estimada. "
            "No representa decisiones individuales de cada colocador."
        )

        if distribucion:
            st.plotly_chart(
                crear_cancha(distribucion),
                width="stretch",
                key=f"cancha_j7_{jugador_id}_{temporada_id}",
                config={
                    "displayModeBar": False,
                    "scrollZoom": False
                }
            )
        else:
            st.info(
                "No hay distribución disponible "
                "para esta selección."
            )

        return

    if numero_jornada == 6:
        import sqlite3

        st.markdown("#### Jornada 6 · Jatorkide")

        with sqlite3.connect(
            "file:volley_chamar.db?mode=ro",
            uri=True
        ) as conexion:
            jugador = conexion.execute(
                "SELECT nombre FROM jugadores WHERE id = ?",
                (jugador_id,)
            ).fetchone()

            partido = conexion.execute(
                "SELECT id FROM partidos WHERE jornada = 6",
            ).fetchone()

            datos = None

            if partido:
                datos = conexion.execute(
                    """
                    SELECT
                        total_acciones,
                        valoracion_doble_positiva,
                        valoracion_positiva
                    FROM estadisticas_fundamento
                    WHERE partido_id = ?
                      AND jugador_id = ?
                      AND LOWER(fundamento) = 'colocación'
                    """,
                    (partido[0], jugador_id)
                ).fetchone()

        nombre = jugador[0] if jugador else ""

        if nombre in ("Abel Marina", "Leo Portillo") and datos:
            total = int(datos[0] or 0)
            perfectas = int(datos[1] or 0)
            positivas = int(datos[2] or 0)

            calidad = (
                100 * (perfectas + positivas) / total
                if total else 0
            )

            st.markdown(f"**Colocador: {nombre}**")

            st.markdown("""
            <style>
            .chv-j6-card {
                background: linear-gradient(145deg, #22242d, #12141b);
                border: 1px solid #3a3d47;
                border-top: 4px solid #ffd600;
                border-radius: 15px;
                padding: 22px 12px;
                text-align: center;
                min-height: 145px;
                margin-bottom: 12px;
            }
            .chv-j6-label {
                color: #d5d6dc;
                font-size: 13px;
                font-weight: 700;
                margin-bottom: 14px;
            }
            .chv-j6-value {
                color: white;
                font-size: 34px;
                font-weight: 800;
            }
            .chv-j6-subtitle {
                color: #a7aab5;
                font-size: 11px;
                margin-top: 8px;
            }
            </style>
            """, unsafe_allow_html=True)

            def tarjeta_j6(titulo, valor, subtitulo):
                st.markdown(
                    f"""
                    <div class="chv-j6-card">
                        <div class="chv-j6-label">{titulo}</div>
                        <div class="chv-j6-value">{valor}</div>
                        <div class="chv-j6-subtitle">{subtitulo}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("#### 🏐 Rendimiento del colocador")

            c1, c2, c3 = st.columns(3)

            with c1:
                tarjeta_j6(
                    "🏐 COLOCACIONES OFICIALES",
                    total,
                    "Total de J6"
                )

            with c2:
                tarjeta_j6(
                    "🎯 CALIDAD POSITIVA",
                    f"{calidad:.1f}%",
                    "Calidad oficial de J6"
                )

            with c3:
                tarjeta_j6(
                    "📊 COLOCACIONES POSITIVAS",
                    perfectas + positivas,
                    "Perfectas + positivas"
                )

        else:
            st.info(
                "No hay estadísticas individuales de colocación "
                "registradas para este jugador en J6."
            )

        st.markdown("##### Distribución ofensiva por zonas")

        distribucion, ataques = calcular_distribucion(
            sets,
            jornada=6
        )

        st.metric("Ataques analizados", ataques)

        st.caption(
            "J6 — Distribución ofensiva estimada del equipo. "
            "No representa decisiones individuales de cada colocador."
        )

        if distribucion:
            st.plotly_chart(
                crear_cancha(distribucion),
                width="stretch",
                key=f"cancha_j6_{jugador_id}_{temporada_id}"
            )
        else:
            st.info("No hay distribución disponible.")

        return

    # INTEGRACION_VISUAL_J5_ACENVOLLEY
    if numero_jornada == 5:
        import sqlite3

        with sqlite3.connect(
            "file:volley_chamar.db?mode=ro",
            uri=True
        ) as conexion:
            fila = conexion.execute(
                "SELECT nombre FROM jugadores WHERE id = ?",
                (jugador_id,)
            ).fetchone()

        nombre = fila[0] if fila else ""

        st.markdown("#### Jornada 5 · Acenvolley")

        if nombre in COLOCACIONES_J5:
            datos = COLOCACIONES_J5[nombre]

            calidad = (
                100 * (
                    datos["perfectas"] + datos["positivas"]
                ) / datos["total"]
                if datos["total"] else 0
            )

            st.markdown(f"**Colocador: {nombre}**")

            st.markdown("""
            <style>
            .chv-j5-card {
                background: linear-gradient(145deg, #22242d, #12141b);
                border: 1px solid #3a3d47;
                border-top: 4px solid #ffd600;
                border-radius: 15px;
                padding: 22px 12px;
                text-align: center;
                min-height: 145px;
                margin-bottom: 12px;
            }
            .chv-j5-label {
                color: #d5d6dc;
                font-size: 13px;
                font-weight: 700;
                margin-bottom: 14px;
            }
            .chv-j5-value {
                color: white;
                font-size: 34px;
                font-weight: 800;
            }
            .chv-j5-subtitle {
                color: #a7aab5;
                font-size: 11px;
                margin-top: 8px;
            }
            </style>
            """, unsafe_allow_html=True)

            def tarjeta_j5(titulo, valor, subtitulo):
                st.markdown(
                    f"""
                    <div class="chv-j5-card">
                        <div class="chv-j5-label">{titulo}</div>
                        <div class="chv-j5-value">{valor}</div>
                        <div class="chv-j5-subtitle">{subtitulo}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("#### 🏐 Rendimiento del colocador")

            c1, c2, c3 = st.columns(3)

            with c1:
                tarjeta_j5(
                    "🏐 COLOCACIONES OFICIALES",
                    datos["total"],
                    "Total de J5"
                )

            with c2:
                tarjeta_j5(
                    "🎯 CALIDAD POSITIVA",
                    f"{calidad:.1f}%",
                    "Calidad oficial de J5"
                )

            with c3:
                tarjeta_j5(
                    "📊 COLOCACIONES POSITIVAS",
                    datos["perfectas"] + datos["positivas"],
                    "Perfectas + positivas"
                )

            if seleccion != "Partido completo":
                st.markdown(
                    "ⓘ **Información de las estadísticas**",
                    help=(
                        "Las colocaciones oficiales corresponden "
                        "al partido completo, no al set seleccionado. "
                        "La cancha representa la distribución "
                        "ofensiva colectiva del equipo."
                    )
                )

        distribucion, ataques = calcular_distribucion(
            sets,
            jornada=5
        )

        st.markdown(
            "##### Distribución ofensiva estimada por zonas"
        )

        st.metric("Ataques analizados", ataques)

        st.plotly_chart(
            crear_cancha(distribucion),
            width="stretch",
            key=f"cancha_{jugador_id}_{temporada_id}",
            config={
                "displayModeBar": False,
                "scrollZoom": False
            }
        )

        return

    # INTEGRACION_VISUAL_J4_PALENCIA
    if numero_jornada == 4:
        import sqlite3

        with sqlite3.connect(
            "file:volley_chamar.db?mode=ro",
            uri=True
        ) as conexion:
            fila = conexion.execute(
                "SELECT nombre FROM jugadores WHERE id = ?",
                (jugador_id,)
            ).fetchone()

        nombre = fila[0] if fila else ""

        st.markdown("#### Jornada 4 · CYL Palencia 2028")

        if nombre in COLOCACIONES_J4:
            datos = COLOCACIONES_J4[nombre]

            calidad = (
                100
                * (datos["perfectas"] + datos["positivas"])
                / datos["total"]
                if datos["total"] else 0
            )

            st.markdown(f"**Colocador: {nombre}**")

    
        # Tarjetas individuales de rendimiento — J4
        st.markdown("""
        <style>
        .chamar-stat-card {
            background: linear-gradient(145deg, #22242d, #12141b);
            border: 1px solid #3a3d47;
            border-top: 4px solid #ffd600;
            border-radius: 15px;
            padding: 20px 12px;
            text-align: center;
            min-height: 145px;
            margin-bottom: 12px;
        }
        .chamar-stat-label {
            color: #d5d6dc;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: .4px;
            margin-bottom: 14px;
        }
        .chamar-stat-value {
            color: white;
            font-size: 34px;
            font-weight: 800;
        }
        .chamar-stat-subtitle {
            color: #a7aab5;
            font-size: 11px;
            margin-top: 8px;
        }
        </style>
        """, unsafe_allow_html=True)

        def tarjeta_j4(titulo, valor, subtitulo=""):
            st.markdown(
                f"""
                <div class="chamar-stat-card">
                    <div class="chamar-stat-label">{titulo}</div>
                    <div class="chamar-stat-value">{valor}</div>
                    <div class="chamar-stat-subtitle">{subtitulo}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("#### 🏐 Rendimiento del colocador")

        c1, c2, c3 = st.columns(3)

        with c1:
            tarjeta_j4(
                "🏐 COLOCACIONES OFICIALES",
                datos["total"],
                "Total del partido"
            )

        with c2:
            tarjeta_j4(
                "🎯 CALIDAD POSITIVA",
                f"{calidad:.1f}%",
                "Colocaciones positivas"
            )

        with c3:
            tarjeta_j4(
                "🛡️ DEFENSAS",
                datos["defensas"],
                "Acciones defensivas"
            )

        st.markdown("#### 📊 Otras estadísticas de la jornada")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            tarjeta_j4("🎾 SAQUES", datos["saques"])

        with c2:
            tarjeta_j4(
                "❌ ERRORES DE SAQUE",
                datos["errores_saque"]
            )

        with c3:
            tarjeta_j4("⚡ ATAQUES", datos["ataques"])

        with c4:
            tarjeta_j4("🏆 PUNTOS", datos["puntos"])

        if seleccion != "Partido completo":
            st.markdown(
                "ⓘ **Información sobre las estadísticas**",
                help=(
                    "Las colocaciones individuales oficiales están "
                    "disponibles para el partido completo, "
                    "pero no desglosadas por set. "
                    "Los indicadores individuales corresponden "
                    "al total de la jornada."
                )
            )

        distribucion, ataques = calcular_distribucion(
            sets,
            jornada=4
        )

        st.markdown(
            "##### Distribución ofensiva estimada por zonas"
        )

        st.metric(
            "Ataques analizados",
            ataques
        )



        st.plotly_chart(
            crear_cancha(distribucion),
            width="stretch",
            key=f"cancha_{jugador_id}_{temporada_id}",
            config={
                "displayModeBar": False,
                "scrollZoom": False
            }
        )

        return

    # INTEGRACION_SEGURA_VALLADOLID_J3
    # J3 utiliza el modelo de participación ya existente.
    # No modifica la cancha ni los cálculos de J1/J2.
    if numero_jornada == 3:
        import sqlite3

        from participacion_colocadores_j3 import (
            TITULARES,
            COLOCACIONES,
        )
        from distribucion_colocadores_j3 import obtener_resumen

        with sqlite3.connect(
            "file:volley_chamar.db?mode=ro",
            uri=True,
        ) as conexion:
            fila = conexion.execute(
                "SELECT nombre FROM jugadores WHERE id = ?",
                (jugador_id,),
            ).fetchone()

        nombre = fila[0] if fila else ""


        # CHV_TARJETAS_J3_V1
        st.markdown("""
        <style>
        .chv-j3-card {
            background: linear-gradient(145deg, #22242d, #17191f);
            border: 1px solid #41434e;
            border-left: 5px solid #FFD700;
            border-radius: 14px;
            padding: 22px;
            min-height: 155px;
            margin-bottom: 12px;
        }
        .chv-j3-label {
            color: #BFC0C8;
            font-size: 13px;
            font-weight: 800;
            margin-bottom: 16px;
        }
        .chv-j3-value {
            color: white;
            font-size: 37px;
            font-weight: 800;
            line-height: 1.2;
        }
        .chv-j3-subtitle {
            color: #A9ABB5;
            font-size: 12px;
            margin-top: 8px;
        }
        
/* CHV_J3_CENTRADO_FINAL */

.chv-j3-card {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    text-align: center !important;
}

.chv-j3-label,
.chv-j3-value,
.chv-j3-subtitle {
    width: 100% !important;
    text-align: center !important;
}

</style>
        """, unsafe_allow_html=True)

        st.markdown("#### Jornada 3 · Valladolid")

        if nombre in COLOCACIONES:
            resumen_j3 = obtener_resumen(nombre, sets)
            oficiales = resumen_j3[
                "colocaciones_oficiales_partido"
            ]

            st.markdown(f"**Colocador: {nombre}**")


            calidad = (
                100 * (
                    oficiales["perfectas"]
                    + oficiales["positivas"]
                ) / oficiales["total"]
                if oficiales["total"] else 0
            )

            estimadas = resumen_j3[
                "colocaciones_estimadas_seleccion"
            ]

            indicadores = [
                (
                    "🏐 COLOCACIONES J3",
                    str(oficiales["total"]),
                    "Total oficial del partido",
                ),
                (
                    "🎯 CALIDAD POSITIVA",
                    f"{calidad:.1f}%",
                    "Calidad oficial de J3",
                ),
                (
                    "📊 COLOCACIONES ESTIMADAS",
                    f"{estimadas:.1f}",
                    "Selección actual",
                ),
            ]

            columnas = st.columns(3)

            for columna, (etiqueta, valor, detalle) in zip(
                columnas, indicadores
            ):
                with columna:
                    st.markdown(
                        f"""
                        <div class="chv-j3-card">
                            <div class="chv-j3-label">
                                {etiqueta}
                            </div>
                            <div class="chv-j3-value">
                                {valor}
                            </div>
                            <div class="chv-j3-subtitle">
                                {detalle}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            titulares = [
                str(numero)
                for numero, titular in TITULARES.items()
                if titular == nombre
            ]

            st.caption(
                "Sets como titular: "
                + (", ".join(titulares) if titulares else "Ninguno")
            )


            # CHV_J3_SETS_V3
            st.markdown("##### Participación estimada por set")

            st.markdown("""
            <style>
            .chv-set-card {
                background: linear-gradient(145deg, #22242d, #17191f);
                border: 1px solid #41434e;
                border-top: 3px solid #FFD700;
                border-radius: 12px;
                padding: 18px 8px;
                text-align: center;
                min-height: 125px;
            }
            .chv-set-title {
                color: #BFC0C8;
                font-size: 13px;
                font-weight: 800;
            }
            .chv-set-number {
                color: white;
                font-size: 30px;
                font-weight: 800;
                margin: 8px 0;
            }
            .chv-set-status {
                color: #FFD700;
                font-size: 11px;
                font-weight: 700;
            }
            </style>
            """, unsafe_allow_html=True)

            detalle_sets = resumen_j3["estimacion_por_set"]
            columnas_sets = st.columns(5, gap="small")

            for columna, (numero_set, cantidad) in zip(
                columnas_sets,
                detalle_sets.items(),
            ):
                es_titular = TITULARES[numero_set] == nombre
                estado = "TITULAR" if es_titular else "NO TITULAR"

                with columna:
                    st.markdown(
                        f"""
                        <div class="chv-set-card">
                            <div class="chv-set-title">
                                SET {numero_set}
                            </div>
                            <div class="chv-set-number">
                                {cantidad:.1f}
                            </div>
                            <div class="chv-set-status">
                                {estado}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )



        else:
            st.info(
                "La distribución de Valladolid está disponible "
                "como estadística colectiva."
            )

        # Se conserva la función original de dibujo de cancha.
        distribucion, ataques = calcular_distribucion(
            sets,
            jornada=3,
        )

        st.markdown(
            "##### Distribución ofensiva del equipo"
        )


        from distribucion_colocadores_j3 import ATAQUES_SET

        ataques_desglose = sum(
            ATAQUES_SET[numero]
            for numero in sets
        )

        if seleccion == "Partido completo":
            st.metric(
                "Ataques del partido · Data Volley",
                ataques,
            )
            None




        else:
            st.metric(
                "Ataques registrados en el set",
                ataques_desglose,
            )
            None






        if seleccion != "Partido completo":
            None






        if distribucion:
            st.plotly_chart(
                crear_cancha(distribucion),
                width="stretch",
                key=f"cancha_{jugador_id}_{temporada_id}", config={"displayModeBar": False, "scrollZoom": False},
            )
        else:
            st.info(
                "No hay una distribución por zonas disponible "
                "para esta selección. No se mostrarán "
                "porcentajes sin datos suficientes."
            )

        None





        return

    if numero_jornada == 2:
        from sqlite3 import connect

        with connect(
            "file:volley_chamar.db?mode=ro",
            uri=True
        ) as conexion:
            jugador = conexion.execute(
                "SELECT nombre FROM jugadores WHERE id = ?",
                (jugador_id,)
            ).fetchone()

        nombre = jugador[0] if jugador else ""

        if nombre in ("Abel Marina", "Leo Portillo"):
            # J2: distribución colectiva mientras no exista
            # una reconstrucción individual verificada.
            distribucion, ataques = calcular_distribucion(
                sets,
                jornada=numero_jornada,
            )

        else:
            distribucion, ataques = calcular_distribucion(
                sets,
                jornada=numero_jornada,
            )
    else:
        distribucion, ataques = calcular_distribucion(
            sets,
            jornada=numero_jornada,
        )

    st.metric("Ataques analizados", ataques)

    if numero_jornada == 1:
        st.caption(
            "J1 — Modelo experimental. La distribución por zonas "
            "es una estimación basada en los datos de Data Volley."
        )
    else:
        st.caption(
            "J2 — Distribución colectiva del equipo. "
            "Los porcentajes globales no representan "
            "las decisiones de un colocador individual."
        )

    if distribucion or numero_jornada == 2:
        st.plotly_chart(
            crear_cancha(distribucion),
            width="stretch",
            key=f"cancha_{jugador_id}_{temporada_id}", config={"displayModeBar": False, "scrollZoom": False},
        )
    else:
        st.info(
            "Disponemos del número de ataques de este set, "
            "pero no de su distribución por zonas. "
            "Selecciona 'Partido completo' para visualizar "
            "la distribución colectiva de Covadonga."
        )

    if numero_jornada == 1 and seleccion != "Partido completo":
        titular = DATOS_J1[sets[0]]["titular"]
        st.caption(f"Colocador titular del set: {titular}")

    st.info(
        "Esta visualización describe la distribución ofensiva "
        "del equipo. No constituye una medición individual "
        "del colocador seleccionado."
    )
