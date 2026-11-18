
import streamlit as st
from distribucion_ofensiva import mostrar_distribucion_ofensiva


def mostrar_perfil_colocador(partidos, resumen, jugador_id, temporada_id):
    """Muestra las estadísticas especializadas del colocador."""

    colocacion = resumen.get("Colocación", {})

    total = int(colocacion.get("acciones") or 0)

    if total == 0:
        st.info("Todavía no hay estadísticas de colocación.")
        return

    st.markdown("""
    <style>
    .chv-colocador-titulo {
        color: #FFD700;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 18px;
    }
    .chv-colocador-card {
        background: linear-gradient(145deg, #22242d, #17191f);
        border: 1px solid #41434e;
        border-left: 4px solid #FFD700;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 12px;
    }
    .chv-colocador-label {
        color: #BFC0C8;
        font-size: 13px;
        font-weight: 700;
    }
    .chv-colocador-valor {
        color: #FFFFFF;
        font-size: 36px;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="chv-colocador-titulo">'
        '🎯 Dirección de juego'
        '</div>',
        unsafe_allow_html=True
    )

    columnas = st.columns(3)

    indicadores = [
        ("🏐 COLOCACIONES", total),
        ("📅 PARTIDOS", partidos),
        (
            "🎯 CALIDAD POSITIVA",
            f"{colocacion.get('porcentaje_positivo') or 0:.1f}%"
        ),
    ]

    for columna, (etiqueta, valor) in zip(columnas, indicadores):
        with columna:
            st.markdown(
                f"""
                <div class="chv-colocador-card">
                    <div class="chv-colocador-label">{etiqueta}</div>
                    <div class="chv-colocador-valor">{valor}</div>
                </div>
                """,
                unsafe_allow_html=True
            )



    st.markdown("""
    <style>
    .st-key-chv_grafico_marco_3,
    .st-key-chv_grafico_marco_7 {
        border: 1px solid rgba(255, 215, 0, 0.55);
        border-radius: 12px;
        background:
            radial-gradient(
                circle at 95% 5%,
                rgba(255, 215, 0, 0.08),
                transparent 35%
            ),
            #080D12;
        box-shadow:
            0 0 18px rgba(255, 215, 0, 0.07),
            inset 0 0 18px rgba(255, 215, 0, 0.025);
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

    # GRÁFICO DE EVOLUCIÓN DEL COLOCADOR
    import sqlite3
    import plotly.graph_objects as go

    with sqlite3.connect(
        "file:volley_chamar.db?mode=ro",
        uri=True
    ) as conexion:

        registros = conexion.execute("""
            SELECT
                p.jornada,
                p.rival,
                ef.total_acciones,
                ef.valoracion_doble_positiva,
                ef.valoracion_positiva
            FROM estadisticas_fundamento ef
            JOIN partidos p ON p.id = ef.partido_id
            WHERE ef.jugador_id = ?
              AND LOWER(ef.fundamento) = 'colocación'
            ORDER BY p.jornada
        """, (jugador_id,)).fetchall()

    jornadas = []
    porcentajes = []
    rivales = []
    colocaciones = []

    for jornada, rival, total, doble, positiva in registros:
        total = total or 0

        if total <= 0:
            continue

        calidad = ((doble or 0) + (positiva or 0)) / total * 100

        jornadas.append(f"J{jornada}")
        porcentajes.append(calidad)
        rivales.append(rival)
        colocaciones.append(total)

    if jornadas:
        st.markdown(
            '<h3 class="chv-grafico-evolucion-colocador">'
            '📈 Evolución de la calidad de colocación'
            '</h3>',
            unsafe_allow_html=True
        )

    

    # GRÁFICO CINEMATOGRÁFICO — VOLLEY CHAMAR ANALYTICS
    figura = go.Figure()

    # Degradado progresivo bajo la curva.
    if porcentajes:
        figura.add_trace(go.Scatter(
            x=jornadas,
            y=[0] * len(porcentajes),
            mode="lines",
            line=dict(width=0),
            hoverinfo="skip",
            showlegend=False
        ))

        for nivel in range(1, 13):
            factor = nivel / 12
            figura.add_trace(go.Scatter(
                x=jornadas,
                y=[valor * factor for valor in porcentajes],
                mode="lines",
                line=dict(width=0),
                fill="tonexty",
                fillcolor=f"rgba(255,190,0,{0.015 + factor * 0.085:.3f})",
                hoverinfo="skip",
                showlegend=False
            ))

    # Capas de iluminación alrededor de la línea.
    for grosor, opacidad in [
        (24, 0.025),
        (16, 0.045),
        (10, 0.085),
        (6, 0.16)
    ]:
        figura.add_trace(go.Scatter(
            x=jornadas,
            y=porcentajes,
            mode="lines",
            line=dict(
                color=f"rgba(255,205,0,{opacidad})",
                width=grosor
            ),
            hoverinfo="skip",
            showlegend=False
        ))

    # Línea principal.
    figura.add_trace(go.Scatter(
        x=jornadas,
        y=porcentajes,
        mode="lines+markers+text",
        line=dict(color="#FFD700", width=3.5),
        marker=dict(
            size=13,
            color="#FFD700",
            line=dict(color="#FFF7D6", width=2.5)
        ),
        text=[f"{valor:.1f}%" for valor in porcentajes],
        textposition="top center",
        textfont=dict(
            color="#FFFFFF",
            size=15,
            family="Arial"
        ),
        hoverinfo="skip",
        showlegend=False,
        cliponaxis=False
    ))

    figura.update_layout(
        paper_bgcolor="#070C12",
        plot_bgcolor="#070C12",
        font=dict(color="#DCE0E8", size=12),
        height=455,
        margin=dict(l=45, r=35, t=105, b=50),
        xaxis=dict(
            title="Jornada",
            type="category",
            showgrid=False,
            showline=True,
            linecolor="rgba(255,255,255,0.20)",
            fixedrange=True
        ),
        yaxis=dict(
            title="Calidad positiva (%)",
            range=[0, 100],
            tick0=0,
            dtick=20,
            ticksuffix="%",
            gridcolor="rgba(255,255,255,0.09)",
            zeroline=False,
            fixedrange=True
        ),
        showlegend=False,
        dragmode=False,
        hovermode=False,
        clickmode="none"
    )

    # Tarjeta de rendimiento de la última jornada.
    if len(jornadas) >= 2:
        diferencia = porcentajes[-1] - porcentajes[-2]
        signo = "+" if diferencia >= 0 else ""

        resumen_final = (
            f"<b>{jornadas[-1]} · {porcentajes[-1]:.1f}%</b>"
            f"<br>{signo}{diferencia:.1f} pp respecto a {jornadas[-2]}"
            f"<br>{colocaciones[-1]} colocaciones"
        )

        figura.add_annotation(
            x=0.99,
            y=1.25,
            xref="paper",
            yref="paper",
            text=resumen_final,
            showarrow=False,
            align="left",
            xanchor="right",
            font=dict(color="#FFD700", size=13),
            bgcolor="rgba(14,19,27,0.98)",
            bordercolor="#FFD700",
            borderwidth=1,
            borderpad=12
        )


    # Contenedor cinematográfico del gráfico.
    with st.container(key=f"chv_grafico_marco_{jugador_id}"):
        st.plotly_chart(
            figura,
            width="stretch",
            config={
                "staticPlot": True,
                "displayModeBar": False,
                "responsive": True
            },
            key=f"grafico_colocador_{jugador_id}"
        )

    st.caption(
        "La calidad positiva corresponde a colocaciones "
        "valoradas como ++ o + en Data Volley."
    )

    # CANCHA DE DISTRIBUCIÓN OFENSIVA
    mostrar_distribucion_ofensiva(jugador_id, temporada_id)
