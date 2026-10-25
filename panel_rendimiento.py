
import streamlit as st
from html import escape



def mostrar_radar_chv(resumen):
    import plotly.graph_objects as go

    def obtener(fundamento, campo):
        registro = resumen.get(fundamento, {})
        return registro.get(campo)

    ataque = obtener("Ataque", "porcentaje_puntos")
    recepcion = obtener("Recepción", "porcentaje_positivo")
    defensa = obtener("Defensa", "porcentaje_positivo")

    saque_acciones = obtener("Saque", "acciones")
    saque_puntos = obtener("Saque", "puntos")

    if saque_acciones is not None and saque_acciones > 0:
        saque = (saque_puntos or 0) / saque_acciones * 100
    else:
        saque = None

    # No hay intentos totales de bloqueo registrados.
    bloqueo = None

    indicadores = [
        ("Ataque", ataque),
        ("Saque", saque),
        ("Recepción", recepcion),
        ("Defensa", defensa),
        ("Bloqueo", bloqueo),
    ]

    nombres = [nombre for nombre, _ in indicadores]
    valores = [valor for _, valor in indicadores]

    # Figura cerrada únicamente con indicadores disponibles.
    puntos_validos = [
        (nombre, valor)
        for nombre, valor in indicadores
        if valor is not None
    ]

    nombres_validos = [nombre for nombre, _ in puntos_validos]
    valores_validos = [valor for _, valor in puntos_validos]

    if len(puntos_validos) >= 3:
        nombres_validos.append(nombres_validos[0])
        valores_validos.append(valores_validos[0])

    fig = go.Figure()

    # Se muestran marcadores únicamente donde hay datos.
    fig.add_trace(
        go.Scatterpolar(
            r=valores_validos,
            theta=nombres_validos,
            mode="lines+markers",
            connectgaps=False,
            fill="toself" if len(puntos_validos) >= 3 else "none",
            fillcolor="rgba(255, 215, 0, 0.18)",
            line=dict(color="#FFD700", width=3),
            marker=dict(color="#FFD700", size=9),
            name="Rendimiento registrado",
            hovertemplate="%{theta}: %{r:.1f}%<extra></extra>",
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                ticksuffix="%",
                gridcolor="#343640",
                linecolor="#343640",
            ),
            angularaxis=dict(
            categoryorder="array",
            categoryarray=[
                "Ataque",
                "Saque",
                "Recepción",
                "Defensa",
                "Bloqueo",
            ],

                gridcolor="#343640",
                linecolor="#343640",
            ),
        ),
        showlegend=False,
        margin=dict(l=35, r=35, t=20, b=20),
        height=280,
    )

    st.markdown('<div class="chv-panel-header"><div class="chv-panel-header-icon"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#FFD700" stroke-width="2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="#FFD700"/></svg></div><div class="chv-panel-header-text"><div class="chv-panel-header-title">Perfil de rendimiento</div><div class="chv-panel-header-subtitle">Rendimiento por fundamento</div></div></div>', unsafe_allow_html=True)
    st.plotly_chart(fig, width="stretch")

    faltantes = [
        nombre for nombre, valor in indicadores
        if valor is None
    ]

    if faltantes:
        st.caption(
            "Sin porcentaje disponible: "
            + ", ".join(faltantes)
            + ". Los valores ausentes no equivalen a 0 %."
        )



st.markdown(
    """<style>

/* CHV TARJETAS EXTERIORES V1 */

/* Contenedores principales */
.st-key-chv-resumen-panel {
    background: linear-gradient(135deg, #171b24, #10141c);
    border: 1px solid #3b404b;
    border-left: 3px solid #FFD700;
    border-radius: 14px;
    padding: 16px 14px;
    min-height: 510px;
}

/* Encabezados compactos */
.chv-panel-header {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 18px;
}

.chv-panel-header-icon {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

.chv-panel-header-title {
    font-size: 19px !important;
    line-height: 1.25;
    font-weight: 750;
}

.chv-panel-header-subtitle {
    font-size: 12px !important;
    line-height: 1.4;
    color: #A5A9B4;
    margin-top: 4px;
}

/* Tarjetas estadísticas */
.st-key-chv-resumen-panel .chv-card {
    min-height: 125px;
    padding: 14px 12px;
}

.st-key-chv-resumen-panel .chv-card-label {
    font-size: 12px;
}

.st-key-chv-resumen-panel .chv-card-number {
    font-size: 42px;
}

    
/* CHV1995 — Paneles principales */
.st-key-chv-resumen-panel,
.st-key-chv-actividad-panel,
.st-key-chv-radar-panel {
    background: linear-gradient(145deg, #111722, #0b1019);
    border: 1px solid #343b48;
    border-left: 4px solid #FFD700;
    border-radius: 12px;
    padding: 14px !important;
    min-height: 350px;
    box-sizing: border-box;
}


/* CHV1995 — AJUSTE COMPACTO DE TARJETAS */

/* Tarjetas estadísticas más compactas */
.st-key-chv-resumen-panel .chv-card {
    min-height: 105px !important;
    padding: 10px 12px !important;
}

/* Números proporcionados al nuevo tamaño */
.st-key-chv-resumen-panel .chv-card-number {
    font-size: 38px !important;
    line-height: 1.05 !important;
}

/* Etiquetas compactas */
.st-key-chv-resumen-panel .chv-card-label {
    font-size: 11px !important;
    line-height: 1.25 !important;
}

/* Menor separación entre tarjetas */
.st-key-chv-resumen-panel [data-testid="stHorizontalBlock"] {
    gap: 10px !important;
}

/* Menor separación vertical entre filas */
.st-key-chv-resumen-panel [data-testid="stVerticalBlock"] {
    gap: 10px !important;
}

/* Mantener espacio inferior dentro del panel */
.st-key-chv-resumen-panel {
    padding-bottom: 18px !important;
}


/* CHV1995 — AJUSTE COMPACTO FINAL */

/* Tarjetas interiores más compactas */
.st-key-chv-resumen-panel .chv-card {
    min-height: 92px !important;
    padding: 9px 11px !important;
}

/* Números */
.st-key-chv-resumen-panel .chv-card-number {
    font-size: 35px !important;
    line-height: 1 !important;
}

/* Etiquetas */
.st-key-chv-resumen-panel .chv-card-label {
    font-size: 11px !important;
    line-height: 1.2 !important;
}

/* Separación entre tarjetas */
.st-key-chv-resumen-panel [data-testid="stHorizontalBlock"] {
    gap: 8px !important;
}

/* Separación vertical */
.st-key-chv-resumen-panel [data-testid="stVerticalBlock"] {
    gap: 8px !important;
}

/* Menor espacio entre el banner y los paneles */
.st-key-chv-resumen-panel,
.st-key-chv-actividad-panel,
.st-key-chv-radar-panel {
    margin-top: 0 !important;
}

</style>""",
    unsafe_allow_html=True,
)

def mostrar_panel_rendimiento(partidos, resumen):
    """Muestra el resumen visual de actividad de un jugador."""

    def dato(fundamento, campo):
        registro = resumen.get(fundamento, {})
        return registro.get(campo)

    puntos_ataque = dato("Ataque", "puntos") or 0
    puntos_saque = dato("Saque", "puntos") or 0
    puntos_bloqueo = dato("Bloqueo", "puntos") or 0

    puntos_totales = (
        puntos_ataque
        + puntos_saque
        + puntos_bloqueo
    )

    st.markdown("""
    <style>
    .chv-card {
        background: linear-gradient(145deg, #24252D, #15161C);
        border: 1px solid #3B3D46;
        border-top: 3px solid #FFD700;
        border-radius: 12px;
        padding: 14px;
        min-height: 105px;
        box-shadow: 0 8px 24px rgba(0,0,0,.25);
    }

    .chv-card-label {
        color: #B8BAC4;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
    }

    .chv-card-number {
        color: #FFFFFF;
        font-size: 46px;
        font-weight: 850;
        margin-top: 10px;
        line-height: 1.1;
    }

    .chv-yellow {
        color: #FFD700;
    }

    .chv-activity {
        background: linear-gradient(145deg, #202127, #131419);
        border: 1px solid #393B43;
        border-radius: 16px;
        padding: 16px;
        margin-top: 8px;
        margin-bottom: 12px;
    }

    .chv-activity-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #F4F4F5;
        font-size: 15px;
        font-weight: 650;
    }

    .chv-track {
        background: #353741;
        height: 10px;
        border-radius: 20px;
        overflow: hidden;
        margin-top: 6px;
        margin-bottom: 10px;
    }

    .chv-fill {
        background: linear-gradient(90deg, #B58B00, #FFD700);
        height: 100%;
        border-radius: 20px;
    }

    .chv-activity-title {
        color: #FFD700;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
    }
    
/* AJUSTE COMPACTO CHV */
.chv-activity {
    padding: 16px 18px !important;
    margin-top: 8px !important;
    margin-bottom: 8px !important;
}

.chv-activity-title {
    font-size: 12px !important;
    margin-bottom: 14px !important;
    letter-spacing: 1px !important;
}

.chv-activity-row {
    font-size: 13px !important;
}

.chv-track {
    height: 9px !important;
    margin-top: 5px !important;
    margin-bottom: 12px !important;
}

.chv-activity > div:last-child {
    margin-top: 8px !important;
    padding: 9px 12px !important;
    font-size: 12px !important;
}

/* CHV GRID HORIZONTAL V2 */

.chv-activity {
    padding: 18px !important;
}

.chv-activity-title {
    margin-bottom: 16px !important;
}

/* Cada pareja de elementos se organiza horizontalmente. */
.chv-activity {
    display: grid;
    grid-template-columns: 1fr;
}

/* Nombre y estadísticas */
.chv-activity-row {
    display: grid !important;
    grid-template-columns: minmax(105px, 1fr) auto;
    gap: 10px;
    margin-bottom: 3px;
}

/* Barras compactas */
.chv-track {
    height: 9px !important;
    margin-top: 0 !important;
    margin-bottom: 12px !important;
}

.chv-activity > div:last-child {
    width: 100%;
    margin-top: 8px !important;
}

/* CHV1995: escala compacta de encabezados */
.chv-section-heading {
    font-size: 17px !important;
    font-weight: 750 !important;
    line-height: 1.25 !important;
    margin: 4px 0 12px 0 !important;
    color: #F4F4F5 !important;
    white-space: nowrap;
}

.chv-main-heading {
    font-size: 24px !important;
    font-weight: 800 !important;
    line-height: 1.2 !important;
    margin: 0 0 16px 0 !important;
    color: #F4F4F5 !important;
}


/* CHV1995 - Encabezados alineados */
.chv-panel-header {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    min-height: 58px;
    margin: 0 0 12px 0;
}

.chv-panel-header-icon {
    flex: 0 0 22px;
    width: 22px;
    height: 22px;
    margin-top: 1px;
}

.chv-panel-header-text {
    min-width: 0;
}

.chv-panel-header-title {
    color: #F4F4F5;
    font-size: 17px;
    font-weight: 750;
    line-height: 1.2;
}

.chv-panel-header-subtitle {
    color: #9CA3AF;
    font-size: 12px;
    line-height: 1.35;
    margin-top: 4px;
}

</style>
    """, unsafe_allow_html=True)

    st.markdown("<style>" + '\n/* CHV1995 TARJETAS COMPACTAS */\n.st-key-chv-resumen-panel .chv-card {\n    min-height: 105px !important;\n    height: auto !important;\n    padding: 12px 14px !important;\n    box-sizing: border-box !important;\n}\n\n.st-key-chv-resumen-panel .chv-card-label {\n    font-size: 12px !important;\n    line-height: 1.3 !important;\n    margin-bottom: 8px !important;\n}\n\n.st-key-chv-resumen-panel .chv-card-number {\n    font-size: 38px !important;\n    line-height: 1 !important;\n}\n\n.st-key-chv-resumen-panel [data-testid="stVerticalBlock"] {\n    gap: 8px !important;\n}\n' + "</style>", unsafe_allow_html=True)


    st.markdown("""
    <style>

/* CHV1995 - ESPACIO INFERIOR TARJETAS V1 */
.st-key-chv-resumen-panel [data-testid="stVerticalBlock"] {
    padding-bottom: 16px !important;
}
    </style>
    """, unsafe_allow_html=True)

    def tarjeta(titulo, valor, destacado=False):
        clase = "chv-card-number chv-yellow" if destacado else "chv-card-number"

        st.markdown(
            f"""
            <div class="chv-card">
                <div class="chv-card-label">{escape(str(titulo))}</div>
                <div class="{clase}">{escape(str(valor))}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # CHV1995: estilos visuales de los tres paneles
    st.markdown("""
    <style>

    /* CHV1995 - PANELES VERIFICADOS EN CHROME */

    /* Los tres paneles principales */
    .st-key-chv-resumen-panel,
    .st-key-chv-actividad-panel,
    .st-key-chv-radar-panel {
        background: #171C23 !important;
        border: 1px solid #424851 !important;
        border-left: 4px solid #FFD700 !important;
        border-radius: 15px !important;
        padding: 16px !important;
        box-sizing: border-box !important;
        min-width: 0 !important;
    }

    /* Separación entre encabezados y contenido */
    .st-key-chv-resumen-panel .chv-panel-header,
    .st-key-chv-actividad-panel .chv-panel-header,
    .st-key-chv-radar-panel .chv-panel-header {
        margin-bottom: 18px !important;
    }

    /* Tarjetas del resumen */
    .st-key-chv-resumen-panel .chv-card {
        min-width: 0 !important;
        width: 100% !important;
        box-sizing: border-box !important;
        padding: 12px !important;
    }

    /* Evitar que los títulos desborden */
    .st-key-chv-resumen-panel .chv-card-label {
        font-size: 13px !important;
        line-height: 1.3 !important;
        overflow-wrap: anywhere !important;
    }

    /* Números proporcionados */
    .st-key-chv-resumen-panel .chv-card-number {
        font-size: clamp(28px, 3vw, 48px) !important;
        line-height: 1.1 !important;
    }

    
/* CHV1995 - TARJETAS CENTRADAS V1 */
.st-key-chv-resumen-panel .chv-card {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
}

.st-key-chv-resumen-panel .chv-card-label {
    width: 100% !important;
    text-align: center !important;
}

.st-key-chv-resumen-panel .chv-card-number {
    width: 100% !important;
    text-align: center !important;
}

</style>
    """, unsafe_allow_html=True)


    st.markdown("""
<style>

/* CHV1995 - AJUSTE COMPACTO DE ESPACIADO */

/* Reducir el espacio entre encabezados y contenido */
.st-key-chv-resumen-panel .chv-panel-header,
.st-key-chv-actividad-panel .chv-panel-header,
.st-key-chv-radar-panel .chv-panel-header {
    margin-bottom: 0px !important;
}

/* Subir las tarjetas del resumen */
.st-key-chv-resumen-panel [data-testid="stHorizontalBlock"] {
    margin-top: 0px !important;
}

/* Subir el contenido de actividad */
.st-key-chv-actividad-panel .chv-panel-header + div {
    margin-top: -12px !important;
}

/* Mantener el radar con un espacio visual equilibrado */
.st-key-chv-radar-panel .chv-panel-header + div {
    margin-top: -8px !important;
}
</style>
""", unsafe_allow_html=True)

    columna_resumen, columna_actividad, columna_radar = st.columns([1.15, 1.15, 1.10], gap="small")

    with columna_resumen:
        with st.container(key="chv-resumen-panel"):
            st.markdown('<div class="chv-panel-header"><div class="chv-panel-header-icon"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#FFD700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 21h8M12 17v4M7 4h10v6a5 5 0 0 1-10 0V4Z"/><path d="M7 6H4v3a4 4 0 0 0 4 4M17 6h3v3a4 4 0 0 1-4 4"/></svg></div><div class="chv-panel-header-text"><div class="chv-panel-header-title">Resumen de temporada</div><div class="chv-panel-header-subtitle">Estadísticas principales del jugador</div></div></div>', unsafe_allow_html=True)

            columna_1, columna_2 = st.columns(2)

            with columna_1:
                tarjeta("🏐 Partidos analizados", partidos)

            with columna_2:
                tarjeta("⚡ Puntos directos", puntos_totales, True)


            st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
            ataque, saque, bloqueo = st.columns(3)

            with ataque:
                tarjeta("PUNTOS DE ATAQUE", puntos_ataque)

            with saque:
                tarjeta("PUNTOS DE SAQUE", puntos_saque)

            with bloqueo:
                tarjeta("PUNTOS DE BLOQUEO", puntos_bloqueo)


    with columna_actividad:
        with st.container(key="chv-actividad-panel"):
            st.markdown('<div class="chv-panel-header"><div class="chv-panel-header-icon"><svg viewBox="0 0 24 24" width="22" height="22" fill="#F4F4F5"><rect x="3" y="13" width="4" height="8"/><rect x="10" y="8" width="4" height="13"/><rect x="17" y="3" width="4" height="18"/></svg></div><div class="chv-panel-header-text"><div class="chv-panel-header-title">Distribución de actividad</div><div class="chv-panel-header-subtitle">Número total de acciones por fundamento</div></div></div>', unsafe_allow_html=True)

            dimensiones = [
                ("⚡ Ataque", dato("Ataque", "acciones")),
                ("🏐 Saque", dato("Saque", "acciones")),
                ("🛡️ Recepción", dato("Recepción", "acciones")),
                ("🏃 Defensa", dato("Defensa", "acciones")),
            ]

            total_acciones = sum(
                valor for _, valor in dimensiones
                if isinstance(valor, (int, float))
            )

            barras = []

            for nombre, valor in dimensiones:
                if valor is None:
                    texto = "Sin registro"
                    porcentaje = 0
                else:
                    porcentaje = (
                        valor / total_acciones * 100
                        if total_acciones > 0
                        else 0
                    )
                    texto = f"{valor} · {porcentaje:.1f}%"

                barras.append(f"""
                <div class="chv-activity-row">
                    <span>{escape(nombre)}</span>
                    <span>{escape(texto)}</span>
                </div>
                <div class="chv-track">
                    <div class="chv-fill"
                         style="width:{porcentaje:.1f}%"></div>
                </div>
                """)

            puntos_bloqueo = dato("Bloqueo", "puntos")
            texto_bloqueo = (
                "Sin registro"
                if puntos_bloqueo is None
                else f"{puntos_bloqueo} puntos"
            )

            barras.append(f"""
            <div class="chv-activity-row">
                <span>✋ Bloqueo</span>
                <span>{escape(texto_bloqueo)}</span>
            </div>
            <div class="chv-track">
                <div class="chv-fill" style="width:{min(100, max(0, (puntos_bloqueo or 0) * 10)):.1f}%"></div>
            </div>
            """)

            st.markdown(
                '<div class="chv-activity">'
                '<div class="chv-activity-title">'
                'ACTIVIDAD REGISTRADA · TEMPORADA'
                '</div>'
                + "".join(
                    linea.strip()
                    for barra in barras
                    for linea in barra.splitlines()
                )
                + f"""
                <div style="
                    margin-top:16px;
                    padding:14px;
                    background:#242630;
                    border-radius:10px;
                    color:#ffffff;
                ">
                    📊 Total de acciones cuantificadas:
                    <strong>{total_acciones}</strong>
                </div>
                """
                + '</div>',
                unsafe_allow_html=True
            )



    with columna_radar:
        with st.container(key="chv-radar-panel"):
            mostrar_radar_chv(resumen)



# El radar se integra desde el panel principal.

st.markdown('\n<style>\n/* CHV1995 · Diseño unificado de los tres paneles */\n\n/* Contenedores principales */\n.st-key-chv-resumen-panel,\n.st-key-chv-actividad-panel,\n.st-key-chv-radar-panel {\n    background: linear-gradient(145deg, #171C23, #10141A) !important;\n    border: 1px solid #424851 !important;\n    border-left: 4px solid #FFD700 !important;\n    border-radius: 15px !important;\n    padding: 16px !important;\n    box-sizing: border-box !important;\n}\n\n/* Encabezados */\n.st-key-chv-resumen-panel .chv-panel-header,\n.st-key-chv-actividad-panel .chv-panel-header,\n.st-key-chv-radar-panel .chv-panel-header {\n    margin-bottom: 16px !important;\n}\n\n/* Separación entre tarjetas */\n.st-key-chv-resumen-panel [data-testid="stHorizontalBlock"] {\n    gap: 12px !important;\n}\n\n/* Tarjetas interiores */\n.st-key-chv-resumen-panel .chv-card {\n    min-height: 130px !important;\n    padding: 14px !important;\n}\n\n/* Espaciado vertical */\n.st-key-chv-resumen-panel [data-testid="stVerticalBlock"],\n.st-key-chv-actividad-panel [data-testid="stVerticalBlock"],\n.st-key-chv-radar-panel [data-testid="stVerticalBlock"] {\n    gap: 12px !important;\n}\n</style>\n', unsafe_allow_html=True)

st.markdown("""
<style>

/* CHV1995 — AJUSTE VISUAL DE PANELES */

.st-key-chv-resumen-panel,
.st-key-chv-actividad-panel,
.st-key-chv-radar-panel {
    background: linear-gradient(145deg, #171C23, #10141A) !important;
    border: 1px solid #424851 !important;
    border-left: 4px solid #FFD700 !important;
    border-radius: 15px !important;
    padding: 16px !important;
    box-sizing: border-box !important;
}

/* Separación entre encabezados y contenido */
.st-key-chv-resumen-panel .chv-panel-header,
.st-key-chv-actividad-panel .chv-panel-header,
.st-key-chv-radar-panel .chv-panel-header {
    margin-bottom: 10px !important;
}

/* Separación vertical de tarjetas */
.st-key-chv-resumen-panel [data-testid="stVerticalBlock"] {
    gap: 10px !important;
}

/* Espacio interior de las tarjetas */
.st-key-chv-resumen-panel .chv-card {
    min-height: 180px !important;
    height: auto !important;
    padding: 16px !important;
    box-sizing: border-box !important;
}

/* Encabezados */
.chv-panel-header-title {
    font-weight: 800 !important;
    color: #F4F4F5 !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<style>' + '\n/* CHV1995_AJUSTE_ESPACIO_BANNER_V1 */\n.st-key-chv-resumen-panel,\n.st-key-chv-actividad-panel,\n.st-key-chv-radar-panel {\n    margin-top: -24px !important;\n}\n' + '</style>', unsafe_allow_html=True)




st.markdown("""<style>
/* CHV1995 - TIPOGRAFIA COMPACTA DEL RESUMEN */
.st-key-chv-resumen-panel .chv-card-number {
    font-size: 36px !important;
    line-height: 1.05 !important;
    margin-top: 6px !important;
}
</style>""", unsafe_allow_html=True)
