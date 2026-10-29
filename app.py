from estadisticas_detalladas import mostrar_estadisticas_detalladas
from pathlib import Path
from panel_rendimiento import mostrar_panel_rendimiento
import streamlit as st
import sqlite3
import hmac

st.set_page_config(
    page_title="Volley Chamar",
    page_icon="🏐",
    layout="wide"
)

st.markdown('\n<style>\n/* VOLLEY CHAMAR - AJUSTE ESPACIO SUPERIOR */\n\n[data-testid="stMainBlockContainer"],\n.block-container {\n    padding-top: 2.5rem !important;\n}\n\n</style>\n', unsafe_allow_html=True)
if "admin_autenticado" not in st.session_state:
    st.session_state["admin_autenticado"] = False

# Base de datos
def es_version_publica():
    import os
    return os.environ.get("VOLLEY_PUBLICO") == "1"


def conectar():
    if es_version_publica():
        ruta = Path("volley_chamar_publica.db").resolve()
        return sqlite3.connect(
            ruta.as_uri() + "?mode=ro",
            uri=True
        )

    return sqlite3.connect("volley_chamar.db")


def preparar_base_datos():
    with conectar() as conexion:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS equipos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE
            )
        """)

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS temporadas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                equipo_id INTEGER NOT NULL,
                UNIQUE(nombre, equipo_id)
            )
        """)

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS jugadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                posicion TEXT NOT NULL,
                dorsal INTEGER NOT NULL,
                temporada_id INTEGER NOT NULL
            )
        """)

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS partidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temporada_id INTEGER NOT NULL,
                rival TEXT NOT NULL,
                fecha TEXT NOT NULL,
                resultado TEXT NOT NULL
            )
        """)



if not es_version_publica():
    preparar_base_datos()




# Seguridad: la versión pública nunca tiene privilegios administrativos.
if es_version_publica():
    st.session_state["admin_autenticado"] = False

if not es_version_publica():
    # Acceso de administrador
    st.sidebar.divider()

    if not st.session_state["admin_autenticado"]:
        with st.sidebar.expander("🔐 Acceso administrador"):
            with st.form("formulario_login"):
                password = st.text_input(
                    "Contraseña",
                    type="password"
                )

                iniciar = st.form_submit_button("Iniciar sesión")

                if iniciar:
                    if hmac.compare_digest(
                        password,
                        st.secrets["ADMIN_PASSWORD"]
                    ):
                        st.session_state["admin_autenticado"] = True
                        st.rerun()
                    else:
                        st.error("Contraseña incorrecta")

    else:
        st.sidebar.success("🔓 Modo administrador")

        if st.sidebar.button("Cerrar sesión"):
            st.session_state["admin_autenticado"] = False
            st.rerun()

menu = st.sidebar.radio(
    "Menú principal",
    ["Inicio", "Equipos", "Temporadas", "Jugadores", "Partidos", "Estadísticas"]
)

if menu == "Inicio":
    import base64
    import textwrap

    with open("assets/equipo_chamar.png", "rb") as imagen:
        imagen_base64 = base64.b64encode(imagen.read()).decode()

    st.markdown(
        textwrap.dedent("""
        <style>
        .chamar-hero {
            position: relative;
            min-height: 540px;
            border-radius: 14px;
            overflow: hidden;
            background-image:
                linear-gradient(
                    90deg,
                    rgba(0,0,0,0.92) 0%,
                    rgba(0,0,0,0.65) 38%,
                    rgba(0,0,0,0.15) 100%
                ),
                linear-gradient(
                    0deg,
                    rgba(10,10,10,1) 0%,
                    rgba(10,10,10,0) 55%
                ),
                url("data:image/png;base64,IMAGEN_BASE64");

            background-size: cover;
            background-position: center;
            display: flex;
            align-items: center;
            padding: 48px;
        }

        .chamar-hero-content {
            position: relative;
            z-index: 2;
            max-width: 650px;
        }

        .chamar-eyebrow {
            color: #F5D000;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 3px;
            margin-bottom: 22px;
        }

        .chamar-title {
            color: #FFFFFF;
            font-size: clamp(48px, 6vw, 90px);
            font-weight: 900;
            line-height: 0.95;
            letter-spacing: -2px;
            margin: 0 0 26px 0;
        }

        .chamar-subtitle {
            color: #E5E5E5;
            font-size: 19px;
            line-height: 1.6;
            max-width: 430px;
        }

        .chamar-line {
            width: 70px;
            height: 4px;
            background: #F5D000;
            margin-top: 32px;
        }

        .chamar-season {
            margin-top: 24px;
            color: #F5D000;
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 2px;
        }

        @media (max-width: 700px) {
            .chamar-hero {
                min-height: 480px;
                padding: 26px;
                background-position: center;
            }

            .chamar-subtitle {
                font-size: 16px;
            }
        }
        </style>

        <div class="chamar-hero">
            <div class="chamar-hero-content">

                <div class="chamar-eyebrow">
                    CHAMARTÍN VERGARA · VOLEIBOL
                </div>

                <h1 class="chamar-title">
                    VOLLEY<br>CHAMAR
                </h1>

                <div class="chamar-subtitle">
                    El partido termina.<br>
                    El análisis continúa.
                </div>

                <div class="chamar-line"></div>

                <div class="chamar-season">
                    TEMPORADA 2026/2027
                </div>

            </div>
        </div>
        """).replace("IMAGEN_BASE64", imagen_base64).replace("\n        <", "\n<").replace("\n            <", "\n<").replace("\n                <", "\n<").replace("\n    <", "\n<"),
        unsafe_allow_html=True
    )

    st.markdown("### 📊 Centro de rendimiento")
    st.caption("Estadísticas, resultados y evolución del equipo.")

    # Estadísticas reales de la temporada 2026/2027
    with conectar() as conexion:
        temporada = conexion.execute(
            "SELECT id FROM temporadas WHERE nombre = ?",
            ("2026/2027",)
        ).fetchone()

        partidos = []

        if temporada:
            partidos = conexion.execute(
                """
                SELECT jornada, rival, fecha, resultado
                FROM partidos
                WHERE temporada_id = ?
                ORDER BY fecha DESC, jornada DESC
                """,
                (temporada[0],)
            ).fetchall()

    victorias = 0
    derrotas = 0
    partidos_validos = []

    for jornada, rival, fecha, resultado in partidos:
        try:
            sets_favor, sets_contra = map(int, resultado.split("-"))
        except (ValueError, AttributeError):
            continue

        partidos_validos.append((jornada, rival, fecha, resultado))

        if sets_favor > sets_contra:
            victorias += 1
        elif sets_favor < sets_contra:
            derrotas += 1

    total = len(partidos_validos)
    porcentaje = (victorias / total * 100) if total else 0

    # Tarjetas personalizadas del Centro de rendimiento
    st.markdown("""
    <style>
    .chamar-stats {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 16px;
        margin: 24px 0 32px 0;
    }

    .chamar-stat-card {
        background: linear-gradient(145deg, #202126, #15161B);
        border: 1px solid #35363C;
        border-top: 3px solid #F5D000;
        border-radius: 12px;
        padding: 24px 20px;
        min-width: 0;
    }

    .chamar-stat-label {
        color: #B8B8BE;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.3px;
        margin-bottom: 18px;
    }

    .chamar-stat-value {
        color: #FFFFFF;
        font-size: clamp(30px, 3.5vw, 48px);
        font-weight: 800;
        line-height: 1;
    }

    @media (max-width: 900px) {
        .chamar-stats {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 480px) {
        .chamar-stats {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    tarjetas = [
        ("🏐 PARTIDOS", str(total)),
        ("🏆 VICTORIAS", str(victorias)),
        ("❌ DERROTAS", str(derrotas)),
        ("📈 WIN RATE", f"{porcentaje:.0f}%"),
    ]

    contenido_tarjetas = "".join(
        '<div class="chamar-stat-card">'
        '<div class="chamar-stat-label">' + etiqueta + '</div>'
        '<div class="chamar-stat-value">' + valor + '</div>'
        '</div>'
        for etiqueta, valor in tarjetas
    )

    st.markdown(
        '<div class="chamar-stats">' + contenido_tarjetas + '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 📊 Resumen de temporada")

    if partidos_validos:
        from datetime import datetime
        from html import escape

        jornada, rival, fecha, resultado = partidos_validos[0]

        sets_favor, sets_contra = map(int, resultado.split("-"))

        if sets_favor > sets_contra:
            estado = "VICTORIA"
            color_estado = "#F5D000"
        else:
            estado = "DERROTA"
            color_estado = "#E85D5D"

        try:
            fecha_formateada = __import__('datetime').datetime.strptime(
                fecha, "%Y-%m-%d"
            ).strftime("%d/%m/%Y")
        except (ValueError, TypeError):
            fecha_formateada = str(fecha)

        jornada_texto = (
            str(jornada) if jornada is not None else "—"
        )

        rival_seguro = escape(str(rival))
        fecha_segura = escape(fecha_formateada)
        jornada_segura = escape(jornada_texto)

        st.markdown("""
        <style>
        .chamar-match-card {
            background: linear-gradient(135deg, #202126, #111217);
            border: 1px solid #35363C;
            border-left: 4px solid #F5D000;
            border-radius: 12px;
            padding: 32px;
            margin: 20px 0 30px;
        }

        .chamar-match-header {
            color: #F5D000;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 2px;
            margin-bottom: 28px;
        }

        .chamar-match-main {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 20px;
            align-items: center;
            text-align: center;
        }

        .chamar-team-name {
            color: #FFFFFF;
            font-size: clamp(15px, 2vw, 23px);
            font-weight: 800;
        }

        .chamar-score {
            color: #FFFFFF;
            font-size: clamp(36px, 5vw, 64px);
            font-weight: 900;
            white-space: nowrap;
        }

        .chamar-match-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            margin-top: 28px;
            padding-top: 20px;
            border-top: 1px solid #35363C;
            color: #AFAFB6;
            font-size: 13px;
        }

        .chamar-match-status {
            font-weight: 800;
            letter-spacing: 1.5px;
        }

        @media (max-width: 600px) {
            .chamar-match-card {
                padding: 20px;
            }

            .chamar-match-main {
                gap: 8px;
            }

            .chamar-match-footer {
                flex-wrap: wrap;
            }
        }
        </style>
        """, unsafe_allow_html=True)

        tarjeta = f"""
<div class="chamar-match-card">
<div class="chamar-match-header">
ÚLTIMO ENCUENTRO · JORNADA {jornada_segura}
</div>
<div class="chamar-match-main">
<div class="chamar-team-name">CHAMARTÍN VERGARA</div>
<div class="chamar-score">{sets_favor} — {sets_contra}</div>
<div class="chamar-team-name">{rival_seguro.upper()}</div>
</div>
<div class="chamar-match-footer">
<span>{fecha_segura}</span>
<span class="chamar-match-status" style="color:{color_estado};">{estado}</span>
</div>
</div>
"""

        st.markdown(tarjeta, unsafe_allow_html=True)

    else:
        st.info("Todavía no hay partidos registrados en esta temporada.")



elif menu == "Equipos":
    st.header("Gestión de equipos")

    if st.session_state["admin_autenticado"]:
        nombre = st.text_input("Nombre del equipo")

        if st.session_state["admin_autenticado"] and st.button("Registrar equipo"):
            if nombre.strip():
                try:
                    with conectar() as conexion:
                        conexion.execute(
                            "INSERT INTO equipos (nombre) VALUES (?)",
                            (nombre.strip(),)
                        )
                    st.success("Equipo registrado correctamente.")
                except sqlite3.IntegrityError:
                    st.warning("Este equipo ya existe.")
            else:
                st.warning("Introduce el nombre del equipo.")

    with conectar() as conexion:
        equipos = conexion.execute(
            "SELECT nombre FROM equipos ORDER BY nombre"
        ).fetchall()

    st.subheader("Equipos registrados")

    for equipo in equipos:
        st.write("🏐", equipo[0])


elif menu == "Temporadas":
    st.header("Gestión de temporadas")

    with conectar() as conexion:
        equipos = conexion.execute(
            "SELECT id, nombre FROM equipos ORDER BY nombre"
        ).fetchall()

    if equipos:
        opciones = {nombre: identificador for identificador, nombre in equipos}

        if st.session_state["admin_autenticado"]:
            equipo = st.selectbox("Selecciona un equipo", list(opciones))
            temporada = st.text_input(
                "Nombre de la temporada",
                placeholder="2026/2027"
            )        
        
        if st.session_state["admin_autenticado"] and st.button("Registrar temporada"):
            if temporada.strip():
                try:
                    with conectar() as conexion:
                        conexion.execute(
                            "INSERT INTO temporadas (nombre, equipo_id) VALUES (?, ?)",
                            (temporada.strip(), opciones[equipo])
                        )
                    st.success("Temporada registrada correctamente.")
                except sqlite3.IntegrityError:
                    st.warning("Esta temporada ya existe para ese equipo.")
            else:
                st.warning("Introduce una temporada.")
    else:
        st.info("Primero debes registrar un equipo.")

    with conectar() as conexion:
        temporadas_registradas = conexion.execute("""
            SELECT equipos.nombre, temporadas.nombre
            FROM temporadas
            JOIN equipos ON equipos.id = temporadas.equipo_id
            ORDER BY equipos.nombre, temporadas.nombre
        """).fetchall()

    st.subheader("Temporadas registradas")

    if temporadas_registradas:
        for nombre_equipo, nombre_temporada in temporadas_registradas:
            st.write(f"🏐 {nombre_equipo} — {nombre_temporada}")
    else:
        st.info("Todavía no hay temporadas registradas.")


elif menu == "Jugadores":
    st.header("Gestión de jugadores")

    with conectar() as conexion:
        temporadas = conexion.execute("""
            SELECT temporadas.id, equipos.nombre, temporadas.nombre
            FROM temporadas
            JOIN equipos ON equipos.id = temporadas.equipo_id
            ORDER BY equipos.nombre, temporadas.nombre
        """).fetchall()

    if temporadas:
        opciones = {
            f"{equipo} — {temporada} (ID {identificador})": identificador
            for identificador, equipo, temporada in temporadas
        }

        seleccion = st.selectbox("Equipo y temporada", list(opciones))

        if st.session_state.get("admin_autenticado", False):
            with st.expander("➕ Registrar nuevo jugador"):
                nombre = st.text_input("Nombre del jugador")

                posicion = st.selectbox(
                    "Posición",
                    ["Colocador", "Opuesto", "Central", "Receptor", "Líbero"]
                )

                dorsal = st.number_input(
                    "Número de camiseta",
                    min_value=0,
                    max_value=99,
                    step=1
                )

                if st.session_state["admin_autenticado"] and st.button("Registrar jugador"):
                    if nombre.strip():
                        with conectar() as conexion:
                            conexion.execute(
                                """INSERT INTO jugadores
                                (nombre, posicion, dorsal, temporada_id)
                                VALUES (?, ?, ?, ?)""",
                                (nombre.strip(), posicion, dorsal, opciones[seleccion])
                            )
    
                        st.success("Jugador registrado correctamente.")
                    else:
                        st.warning("Introduce el nombre del jugador.")

        with conectar() as conexion:
            jugadores = conexion.execute(
                """SELECT nombre, posicion, dorsal
                FROM jugadores WHERE temporada_id = ?""",
                (opciones[seleccion],)
            ).fetchall()

        jugadores = [
            (str(nombre).strip(), str(posicion).strip(), dorsal)
            for nombre, posicion, dorsal in jugadores
        ]

        st.subheader("🏐 Plantilla del equipo")


        if jugadores:
            from html import escape
            import base64

            seleccion_jugador = st.selectbox(
                "Selecciona un jugador",
                range(len(jugadores)),
                format_func=lambda i: f"#{jugadores[i][2]} · {jugadores[i][0]}",
                key="perfil_jugador_seleccionado"
            )

            nombre, posicion, dorsal = jugadores[seleccion_jugador]

            nombre_seguro = escape(str(nombre))
            posicion_segura = escape(str(posicion))
            dorsal_seguro = escape(str(dorsal))

            st.markdown("""
<style>
.chamar-player-card {
    background: linear-gradient(135deg, #24252B, #111217);
    border: 1px solid #35363C;
    border-left: 5px solid #F5D000;
    border-radius: 14px;
    padding: 40px;
    margin: 25px 0;
}

.chamar-player-eyebrow {
    color: #F5D000;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 25px;
}

.chamar-player-name {
    color: white;
    font-size: clamp(28px, 4vw, 52px);
    font-weight: 900;
    line-height: 1.1;
    margin-bottom: 25px;
}

.chamar-player-info {
    display: flex;
    gap: 18px;
    flex-wrap: wrap;
}

.chamar-player-badge {
    background: #303138;
    border: 1px solid #45464D;
    border-radius: 8px;
    padding: 12px 18px;
    color: white;
    font-size: 14px;
    font-weight: 700;
}

@media (max-width: 600px) {
    .chamar-player-card {
        padding: 25px;
    }
}
</style>
""", unsafe_allow_html=True)

            # CHV1995 — Fotografías individuales
        import base64
        import mimetypes
        import unicodedata

        def normalizar_nombre(texto):
            texto = unicodedata.normalize("NFKD", texto.lower())
            return "".join(
                caracter for caracter in texto
                if not unicodedata.combining(caracter)
            ).strip()

        fotos_jugadores = {
    "leo murciano": "leo_murciano.png.jpg",

    "nano jara": "nano_jara.png.jpg",

            "daniel salido": "daniel_salido.png.jpg",
            "leo portillo": "leo_portillo.png.jpg",
            "rodrigo marchante": "rodrigo_marchante.png",
            "alex salas": "alex_salas.png.jpg",
            "christian sanchez": "christian_sanchez.png.jpeg",
            "ioritz caamano": "ioritz_caamano.png.jpg",
            "sebastian cancino": "sebastian_cancino.png.jpeg",
            "luis anton": "luis_anton.png.jpg",
            "ivan sagues": "ivan_sagues.png.jpg",
            "abel marina": "abel_marina.png.jpg",
            "marcos panero": "marcos_panero.png",
        }

        # Detectar la fotografía de Jhoy sin asumir su extensión.
        fotos_jhoy = sorted(
            ruta for ruta in Path("assets").iterdir()
            if ruta.is_file()
            and ruta.name.lower().startswith("jhoy_castillo")
            and ruta.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")
        )

        if len(fotos_jhoy) == 1:
            fotos_jugadores["jhoy castillo"] = fotos_jhoy[0].name

            nombre_normalizado = normalizar_nombre(nombre)
            nombre_archivo = fotos_jugadores.get(nombre_normalizado)

            foto_jugador = ""

            if nombre_archivo:
                ruta_foto = Path("assets") / nombre_archivo

                if ruta_foto.is_file():
                    tipo_imagen = (
                        mimetypes.guess_type(ruta_foto.name)[0]
                        or "image/jpeg"
                    )

                    imagen_base64 = base64.b64encode(
                        ruta_foto.read_bytes()
                    ).decode("utf-8")

                    foto_jugador = (
                        f"data:{tipo_imagen};base64,{imagen_base64}"
                    )

            # CHV1995 — Encuadres individuales
            posiciones_fotos = {
                "alex salas": 15,
                "christian sánchez": 85,
                "sebastián cancino": 60,
                "ioritz caamaño": 15,
            }

            posicion_foto = posiciones_fotos.get(
                nombre.strip().lower(),
                35
            )

            estilo_foto = (
                "background-image: "
                "linear-gradient(90deg, #1B1C22 0%, "
                "rgba(27,28,34,0.85) 35%, "
                "rgba(27,28,34,0.15) 100%), "
                f"url('{foto_jugador}'); "
                "background-size: cover; "
                "background-position: center 35%;"
                if foto_jugador
                else ""
            )


            ruta_escudo = Path("assets/escudo_chamar.png")
            escudo_banner = ""
            if ruta_escudo.exists():
                import base64
                escudo_banner = (
                    "data:image/png;base64,"
                    + base64.b64encode(ruta_escudo.read_bytes()).decode()
                )

            with conectar() as conexion_banner:
                partidos_registrados_banner = conexion_banner.execute(
                    """
                    SELECT COUNT(*)
                    FROM partidos
                    WHERE temporada_id = ?
                    """,
                    (opciones[seleccion],)
                ).fetchone()[0]

            perfil = f"""
<div class="chv-profile-banner" style="
    display:grid;
    grid-template-columns:43% 25% 32%;
    height:280px;
    width:100%;
    overflow:hidden;
    border-radius:14px;
    border:1px solid #363842;
    border-left:5px solid #FFD700;
    background:#15171E;
    color:white;
">

    <div style="
        position:relative;
        padding:24px 28px;
        display:flex;
        flex-direction:column;
        justify-content:center;
        overflow:hidden;
        background:repeating-linear-gradient(135deg,transparent 0px,transparent 31px,rgba(255,215,0,0.035) 32px,transparent 33px,transparent 65px),radial-gradient(ellipse at 75% 20%,rgba(180,145,50,0.10),transparent 60%),linear-gradient(110deg,#14161D,#20242E);
    ">

        <div style="
            position:absolute;
            right:8px;
            top:0;
            font-size:155px;
            font-weight:900;
            color:transparent;
            -webkit-text-stroke:2px rgba(190,166,79,0.22);
            line-height:1;
            pointer-events:none;
        ">#{dorsal_seguro}</div>

        <div style="
            position:relative;
            color:#FFD700;
            font-size:10px;
            letter-spacing:2px;
            font-weight:800;
            margin-bottom:13px;
        ">
            CHAMARTÍN VERGARA · PERFIL DE JUGADOR
        </div>

        <div style="
            position:relative;
            font-size:clamp(24px,2.6vw,39px);
            font-weight:900;
            line-height:1.05;
            text-transform:uppercase;
            max-width:100%;
            overflow-wrap:anywhere;
        ">
            {nombre_seguro.upper()}
        </div>

        <div style="
            position:relative;
            display:flex;
            gap:10px;
            margin-top:17px;
            font-size:12px;
            font-weight:800;
        ">
            <span style="
                padding:8px 13px;
                border-radius:7px;
                background:#30333D;
                border:1px solid #444752;
            "># {dorsal_seguro}</span>

            <span style="
                padding:8px 13px;
                border-radius:7px;
                background:#30333D;
                border:1px solid #444752;
            ">{posicion_segura.upper()}</span>
        </div>

    </div>

    <div style="
        position:relative;
        height:280px;
        overflow:hidden;
        border-left:5px solid #FFD700;
        border-right:5px solid #FFD700;
        transform:skewX(-9deg);
        background:#252730;
    ">
        <div style="
            position:absolute;
            inset:-18px;
            transform:skewX(9deg);
            background-image:url('{foto_jugador}');
            background-size:cover;
            background-position:center {posicion_foto}%;
            background-repeat:no-repeat;
        "></div>
    </div>

            <div class="chv-banner-details" style="background-image:repeating-linear-gradient(135deg,transparent 0px,transparent 30px,rgba(255,215,0,0.025) 31px,transparent 32px,transparent 62px),linear-gradient(145deg,#171c26,#10141d);
    padding:14px 18px;
    display:grid;
    grid-template-columns:1.35fr 1fr;
    align-items:center;
    gap:14px;
    background:
        repeating-linear-gradient(
            135deg,
            transparent 0px,
            transparent 17px,
            rgba(255,215,0,0.035) 18px,
            transparent 19px
        ),
        linear-gradient(100deg,#191C24,#11151D);
    color:white;
    font-size:12px;
">
    <div style="display:flex;flex-direction:column;min-width:0;">

        <div style="display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid #30343C;">
            <span class="chv-banner-icon" style="display:inline-flex;width:28px;height:28px;min-width:28px;color:#969BA7;align-items:center;justify-content:center;margin-right:12px;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
<circle cx="12" cy="7" r="3.5"/>
<path d="M5 21v-3a7 7 0 0 1 14 0v3H5z"/>
</svg></span>
            <div>
                <div style="color:#969BA7;white-space:nowrap;">POSICIÓN</div>
                <strong style="font-size:15px;">{posicion_segura}</strong>
            </div>
        </div>

        <div style="display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid #30343C;">
            <span class="chv-banner-icon" style="display:inline-flex;width:28px;height:28px;min-width:28px;color:#969BA7;align-items:center;justify-content:center;margin-right:12px;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
<rect x="3" y="5" width="18" height="16" rx="1"/>
<path d="M7 3v4M17 3v4M3 10h18"/>
<path d="M7 14h2M12 14h2M17 14h1M7 18h2M12 18h2"/>
</svg></span>
            <div>
                <div style="color:#969BA7;white-space:nowrap;">TEMPORADA</div>
                <strong style="font-size:15px;">2026/2027</strong>
            </div>
        </div>

        <div style="display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid #30343C;">
            <span class="chv-banner-icon" style="display:inline-flex;width:28px;height:28px;min-width:28px;color:#969BA7;align-items:center;justify-content:center;margin-right:12px;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
<circle cx="12" cy="7" r="3"/>
<circle cx="4.5" cy="10" r="2"/>
<circle cx="19.5" cy="10" r="2"/>
<path d="M6 21v-3a6 6 0 0 1 12 0v3H6z"/>
<path d="M2 20v-3a4 4 0 0 1 3-3.8M22 20v-3a4 4 0 0 0-3-3.8"/>
</svg></span>
            <div>
                <div style="color:#969BA7;white-space:nowrap;">EQUIPO</div>
                <strong style="font-size:15px;white-space:nowrap;">Chamartín Vergara</strong>
            </div>
        </div>

        <div style="display:flex;align-items:center;gap:12px;padding:8px 0;">
            <span class="chv-banner-icon" style="display:inline-flex;width:28px;height:28px;min-width:28px;color:#969BA7;align-items:center;justify-content:center;margin-right:12px;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
<path d="M3 21h18"/>
<rect x="5" y="13" width="3" height="8"/>
<rect x="11" y="8" width="3" height="13"/>
<rect x="17" y="3" width="3" height="18"/>
</svg></span>
            <div>
                <div style="color:#969BA7;white-space:nowrap;">PARTIDOS REGISTRADOS</div>
                <strong style="font-size:15px;">{partidos_registrados_banner}</strong>
            </div>
        </div>

    </div>

    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;min-width:0;width:100%;text-align:center;">
        <img src="{escudo_banner}" style="width:140px;max-width:100%;height:160px;object-fit:contain;transform:translateY(-12px);">
        <div style="font-size:17px;font-weight:900;color:#969BA7;letter-spacing:1px;">CHV1995</div>
        <div style="width:75px;height:4px;background:#FFD700;border-radius:4px;"></div>
    </div>
</div>

</div>
"""

            perfil = "\n".join(
                linea.strip()
                for linea in perfil.splitlines()
                if linea.strip()
            )
            st.markdown(perfil, unsafe_allow_html=True)

            
            import plotly.graph_objects as go

            temporada_perfil_id = opciones[seleccion]

            with conectar() as conexion:
                jugador_perfil = conexion.execute("""
                    SELECT id
                    FROM jugadores
                    WHERE temporada_id = ?
                      AND dorsal = ?
            """, (
                temporada_perfil_id,
                dorsal
            )).fetchone()

                if jugador_perfil:
                    jugador_perfil_id = jugador_perfil[0]

                    registros = conexion.execute("""
                        SELECT
                            ef.fundamento,
                            SUM(ef.total_acciones),
                            SUM(ef.puntos),
                            SUM(ef.errores),
                            SUM(ef.bloqueos_recibidos),
                            SUM(CASE WHEN ef.total_acciones > 0 AND ef.porcentaje_positivo IS NOT NULL THEN ef.total_acciones * ef.porcentaje_positivo END),
                            SUM(CASE WHEN ef.total_acciones > 0 AND ef.porcentaje_positivo IS NOT NULL THEN ef.total_acciones END)
                        FROM estadisticas_fundamento ef
                        JOIN partidos p ON p.id = ef.partido_id
                        WHERE ef.jugador_id = ?
                          AND p.temporada_id = ?
                        GROUP BY ef.fundamento
                    """, (
                        jugador_perfil_id,
                        temporada_perfil_id
                    )).fetchall()

                    referencias = conexion.execute("""
                        SELECT
                            ef.fundamento,
                            ef.jugador_id,
                            SUM(ef.total_acciones),
                            SUM(ef.puntos)
                        FROM estadisticas_fundamento ef
                        JOIN partidos p ON p.id = ef.partido_id
                        WHERE p.temporada_id = ?
                        GROUP BY ef.fundamento, ef.jugador_id
                    """, (temporada_perfil_id,)).fetchall()

                    partidos = conexion.execute("""
                        SELECT COUNT(DISTINCT ef.partido_id)
                        FROM estadisticas_fundamento ef
                        JOIN partidos p ON p.id = ef.partido_id
                        WHERE ef.jugador_id = ?
                          AND p.temporada_id = ?
                    """, (
                        jugador_perfil_id,
                        temporada_perfil_id
                    )).fetchone()[0]
                else:
                    registros = []
                    referencias = []
                    partidos = 0

            if not registros:
                st.info(
                    "Todavía no hay estadísticas registradas "
                    "para este jugador."
                )
            resumen = {
                fila[0]: {
                    "acciones": fila[1],
                    "puntos": fila[2],
                    "errores": fila[3],
                    "bloqueos_recibidos": fila[4],
                    "porcentaje_positivo": (
                        fila[5] / fila[6]
                        if fila[5] is not None and fila[6]
                        else None
                    ),
                    "porcentaje_puntos": (
                        fila[2] / fila[1] * 100
                        if fila[1] and fila[2] is not None
                        else None
                    )
                }
                for fila in registros
            }

            puntos_ataque = resumen.get("Ataque", {}).get("puntos") or 0
            puntos_saque = resumen.get("Saque", {}).get("puntos") or 0
            puntos_bloqueo = resumen.get("Bloqueo", {}).get("puntos") or 0

            mostrar_panel_rendimiento(partidos, resumen)

            # ESTADÍSTICAS DETALLADAS DEL JUGADOR
            with conectar() as conexion:
                conexion.row_factory = sqlite3.Row

                filas_detalladas = conexion.execute(
                    '''
                    SELECT
                        ef.fundamento,
                        SUM(ef.total_acciones) AS acciones,
                        SUM(ef.errores) AS errores,
                        SUM(ef.puntos) AS puntos,
                        SUM(ef.bloqueos_recibidos) AS bloqueos_recibidos,

                        SUM(
                            CASE
                                WHEN ef.total_acciones > 0
                                AND ef.eficiencia_original IS NOT NULL
                                THEN ef.total_acciones * ef.eficiencia_original
                            END
                        ) /
                        NULLIF(
                            SUM(
                                CASE
                                    WHEN ef.total_acciones > 0
                                    AND ef.eficiencia_original IS NOT NULL
                                    THEN ef.total_acciones
                                END
                            ), 0
                        ) AS eficiencia_original,

                        SUM(
                            CASE
                                WHEN ef.total_acciones > 0
                                AND ef.porcentaje_positivo IS NOT NULL
                                THEN ef.total_acciones * ef.porcentaje_positivo
                            END
                        ) /
                        NULLIF(
                            SUM(
                                CASE
                                    WHEN ef.total_acciones > 0
                                    AND ef.porcentaje_positivo IS NOT NULL
                                    THEN ef.total_acciones
                                END
                            ), 0
                        ) AS porcentaje_positivo,

                        SUM(
                            CASE
                                WHEN ef.total_acciones > 0
                                AND ef.porcentaje_excelente IS NOT NULL
                                THEN ef.total_acciones * ef.porcentaje_excelente
                            END
                        ) /
                        NULLIF(
                            SUM(
                                CASE
                                    WHEN ef.total_acciones > 0
                                    AND ef.porcentaje_excelente IS NOT NULL
                                    THEN ef.total_acciones
                                END
                            ), 0
                        ) AS porcentaje_excelente

                    FROM estadisticas_fundamento ef

                    JOIN partidos p
                        ON p.id = ef.partido_id

                    WHERE ef.jugador_id = ?
                      AND p.temporada_id = ?

                    GROUP BY ef.fundamento
                    ''',
                    (
                        jugador_perfil_id,
                        temporada_perfil_id
                    )
                ).fetchall()

            mostrar_estadisticas_detalladas(
                [dict(fila) for fila in filas_detalladas]
            )

            # HISTORIAL INDIVIDUAL DE PARTIDOS
            st.markdown("---")
            st.markdown("### 📅 Historial de partidos")

            with conectar() as conexion:
                partidos_jugador = conexion.execute("""
                    SELECT
                        p.id,
                        p.jornada,
                        p.rival,
                        p.fecha,
                        p.resultado
                    FROM partidos p
                    WHERE p.temporada_id = ?
                      AND EXISTS (
                          SELECT 1
                          FROM estadisticas_fundamento ef
                          WHERE ef.partido_id = p.id
                            AND ef.jugador_id = ?
                      )
                    ORDER BY p.fecha DESC, p.jornada DESC
                """, (
                    temporada_perfil_id,
                    jugador_perfil_id
                )).fetchall()

            if partidos_jugador:
                opciones_partidos = {
                    f"Jornada {jornada} · {rival} · {fecha} · {resultado}": partido_id
                    for partido_id, jornada, rival, fecha, resultado
                    in partidos_jugador
                }


                with conectar() as conexion:
                    historial = conexion.execute(
                        '''
                        SELECT
                            p.jornada,
                            p.rival,
                            p.fecha,
                            p.resultado,
                            COALESCE(SUM(
                                CASE WHEN ef.fundamento IN ('Ataque', 'Saque', 'Bloqueo')
                                THEN ef.puntos ELSE 0 END
                            ), 0),
                            COALESCE(SUM(
                                CASE WHEN ef.fundamento = 'Ataque'
                                THEN ef.puntos ELSE 0 END
                            ), 0),
                            COALESCE(SUM(
                                CASE WHEN ef.fundamento = 'Saque'
                                THEN ef.puntos ELSE 0 END
                            ), 0),
                            COALESCE(SUM(
                                CASE WHEN ef.fundamento = 'Bloqueo'
                                THEN ef.puntos ELSE 0 END
                            ), 0)
                        FROM partidos p
                        JOIN estadisticas_fundamento ef
                            ON ef.partido_id = p.id
                        WHERE ef.jugador_id = ?
                        GROUP BY p.id
                        ORDER BY p.fecha DESC, p.jornada DESC
                        ''',
                        (jugador_perfil_id,)
                    ).fetchall()

                filas_historial = []

                for registro in historial:
                    jornada, rival, fecha, resultado, total, ataque, saque, bloqueo = registro

                    try:
                        fecha_visible = __import__('datetime').datetime.strptime(
                            fecha, "%Y-%m-%d"
                        ).strftime("%d/%m/%Y")
                    except (ValueError, TypeError):
                        fecha_visible = fecha or "—"

                    filas_historial.append({
                        "Jornada": jornada,
                        "Rival": rival,
                        "Fecha": fecha_visible,
                        "Resultado": resultado,
                        "Puntos": total,
                        "Ataque": ataque,
                        "Saque": saque,
                        "Bloqueo": bloqueo,
                    })

                st.dataframe(
                    filas_historial,
                    use_container_width=True,
                    hide_index=True
                )

                st.markdown("#### 🔎 Desglose individual del partido")

                partido_seleccionado = st.selectbox(
                    "Selecciona un partido",
                    list(opciones_partidos),
                    key=f"historial_jugador_{jugador_perfil_id}"
                )

                partido_id = opciones_partidos[partido_seleccionado]

                with conectar() as conexion:
                    estadisticas_partido = conexion.execute("""
                        SELECT
                            fundamento,
                            total_acciones,
                            errores,
                            puntos,
                            bloqueos_recibidos,
                            porcentaje_puntos,
                            eficiencia_original,
                            porcentaje_excelente,
                            porcentaje_positivo
                        FROM estadisticas_fundamento
                        WHERE partido_id = ?
                          AND jugador_id = ?
                        ORDER BY CASE fundamento
                            WHEN 'Ataque' THEN 1
                            WHEN 'Saque' THEN 2
                            WHEN 'Recepción' THEN 3
                            WHEN 'Defensa' THEN 4
                            WHEN 'Bloqueo' THEN 5
                            ELSE 6
                        END
                    """, (
                        partido_id,
                        jugador_perfil_id
                    )).fetchall()

                def valor_perfil(valor, porcentaje=False):
                    if valor is None:
                        return "—"
                    if porcentaje:
                        return f"{valor:g} %"
                    return str(valor)

                filas = []

                for fila in estadisticas_partido:
                    filas.append({
                        "Fundamento": fila[0],
                        "Acciones": valor_perfil(fila[1]),
                        "Errores": valor_perfil(fila[2]),
                        "Puntos": valor_perfil(fila[3]),
                        "Bloqueos recibidos": valor_perfil(fila[4]),
                        "% puntos": valor_perfil(fila[5], True),
                        "Eficiencia PDF": valor_perfil(fila[6], True),
                        "% excelente": valor_perfil(fila[7], True),
                        "% positivo": valor_perfil(fila[8], True),
                    })

                st.dataframe(
                    filas,
                    use_container_width=True,
                    hide_index=True
                )

                st.caption(
                    "— significa dato no registrado o no aplicable. "
                    "Los porcentajes del PDF se conservan sin recalcular."
                )
            else:
                st.info(
                    "Todavía no hay partidos con estadísticas "
                    "individuales para este jugador."
                )

elif menu == "Partidos":
    st.header("Gestión de partidos")
    with conectar() as conexion:
        temporadas = conexion.execute("""
            SELECT temporadas.id, equipos.nombre, temporadas.nombre
            FROM temporadas
            JOIN equipos ON temporadas.equipo_id = equipos.id
            ORDER BY equipos.nombre, temporadas.nombre
        """).fetchall()

    if temporadas:
        opciones = {
            f"{equipo} - {temporada}": temporada_id
            for temporada_id, equipo, temporada in temporadas
        }

        seleccion = st.selectbox(
            "Equipo y temporada",
            list(opciones.keys())
        )

        if st.session_state["admin_autenticado"]:
            with st.expander("➕ Registrar nuevo partido"):
                jornada = st.number_input(
                    "Número de jornada",
                    min_value=1,
                    step=1
                )

                rival = st.text_input("Nombre del rival")
                fecha = st.date_input("Fecha del partido")

                resultado = st.text_input(
                    "Resultado",
                    placeholder="Ejemplo: 3-1"
                )

                if st.button("Registrar partido"):
                    if rival.strip() and resultado.strip():
                        with conectar() as conexion:
                            conexion.execute("""
                                INSERT INTO partidos
                                (temporada_id, jornada, rival, fecha, resultado)
                                VALUES (?, ?, ?, ?, ?)
                            """, (
                                opciones[seleccion],
                                jornada,
                                rival.strip(),
                                fecha.isoformat(),
                                resultado.strip()
                            ))

                        st.success("Partido registrado correctamente.")
                    else:
                        st.warning("Introduce el rival y el resultado.")

        st.subheader("Partidos registrados")

        with conectar() as conexion:
            partidos = conexion.execute("""
                SELECT id, jornada, rival, fecha, resultado
                FROM partidos
                WHERE temporada_id = ?
                ORDER BY jornada ASC, fecha ASC
            """, (opciones[seleccion],)).fetchall()

        if partidos:
            for partido in partidos:
                partido_id, jornada, rival, fecha, resultado = partido

                try:
                    sets_favor, sets_contra = map(int, resultado.split("-"))

                    if sets_favor > sets_contra:
                         estado = "Victoria 🟢"
                    elif sets_favor < sets_contra:
                         estado = "Derrota 🔴"
                    else:
                        estado = "Empate"
                except ValueError:
                    estado = "Resultado no válido"

                st.write(
                    f"Jornada {jornada} | "
                    f"{rival} | "
                    f"{fecha} | "
                    f"{estado} ({resultado})"
                )
                if st.session_state["admin_autenticado"] and st.button("🗑️Eliminar partido", key=f"eliminar_{partido_id}"): 
                    st.session_state[f"confirmar_{partido_id}"] = True
                    st.success("PRUEBA: El botón ha sido pulsado correctamente")

                if st.session_state.get(f"confirmar_{partido_id}", False):
                    st.warning(f"¿Seguro que quieres eliminar el partido contra {rival}?")

                    if st.session_state["admin_autenticado"] and st.button("Confirmar eliminación", key=f"confirmar_eliminar_{partido_id}"):   
                        with conectar() as conexion:
                            conexion.execute(
                                "DELETE FROM partidos WHERE id = ?",
                                (partido_id,)
                            )

                        st.session_state[f"confirmar_{partido_id}"] = False
                        st.rerun()

                    if st.button("Cancelar", key=f"cancelar_{partido_id}"):
                        st.session_state[f"confirmar_{partido_id}"] = False
                        st.rerun()

        else:
            st.info("Todavía no hay partidos registrados.")
    else:
        st.info("Primero debes registrar un equipo y una temporada.")

elif menu == "Estadísticas":
    st.header("🏐 Centro de rendimiento")
    st.caption("VOLLEY CHAMAR · ANÁLISIS DE PARTIDOS")

    with conectar() as conexion:
        partidos_estadisticas = conexion.execute("""
            SELECT id, jornada, rival, fecha, resultado
            FROM partidos
            ORDER BY jornada ASC, fecha ASC
        """).fetchall()

    if not partidos_estadisticas:
        st.info("Todavía no hay partidos registrados.")

    else:
        opciones = {
            f"Jornada {p[1]} · {p[2]}": p
            for p in partidos_estadisticas
        }

        partido_elegido = st.selectbox(
            "Selecciona un partido",
            list(opciones.keys())
        )

        partido = opciones[partido_elegido]
        partido_id, jornada, rival, fecha, resultado = partido

        st.markdown(f"## Jornada {jornada} · {rival}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Resultado", resultado)
        fecha_formateada = "/".join(fecha.split("-")[::-1])
        col2.metric("Fecha", fecha_formateada)
        col3.metric("Jornada", jornada)

        with conectar() as conexion:
            colectivos = conexion.execute("""
                SELECT
                    fundamento,
                    SUM(total_acciones),
                    SUM(errores),
                    SUM(puntos)
                FROM estadisticas_fundamento
                WHERE partido_id = ?
                GROUP BY fundamento
                ORDER BY fundamento
            """, (partido_id,)).fetchall()

            individuales = conexion.execute("""
                SELECT
                    j.dorsal,
                    j.nombre,
                    j.posicion,
                    e.fundamento,
                    e.total_acciones,
                    e.errores,
                    e.puntos,
                    e.bloqueos_recibidos,
                    e.porcentaje_puntos,
                    e.eficiencia_original,
                    e.porcentaje_excelente,
                    e.porcentaje_positivo
                FROM estadisticas_fundamento e
                JOIN jugadores j ON j.id = e.jugador_id
                WHERE e.partido_id = ?
                ORDER BY j.dorsal, e.fundamento
            """, (partido_id,)).fetchall()

        st.divider()
        st.subheader("📊 Rendimiento colectivo")

        if colectivos:
            resumen = [
                {
                    "Fundamento": fila[0],
                    "Acciones": fila[1],
                    "Errores": fila[2],
                    "Puntos": fila[3],
                }
                for fila in colectivos
            ]

            st.dataframe(
                resumen,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Este partido todavía no tiene estadísticas.")

        st.divider()
        st.subheader("👥 Rendimiento individual")

        if individuales:
            fundamentos = sorted(set(fila[3] for fila in individuales))

            fundamento_elegido = st.selectbox(
                "Filtrar por fundamento",
                ["Todos"] + fundamentos
            )

            detalle = []

            for fila in individuales:
                if (
                    fundamento_elegido != "Todos"
                    and fila[3] != fundamento_elegido
                ):
                    continue

                def mostrar(valor, porcentaje=False):
                    if valor is None:
                        return "—"
                    if porcentaje:
                        return f"{valor:g} %"
                    return valor

                registro = {
                    "Dorsal": fila[0],
                    "Jugador": fila[1],
                    "Posición": fila[2],
                    "Fundamento": fila[3],
                    "Acciones": mostrar(fila[4]),
                    "Errores": mostrar(fila[5]),
                    "Puntos": mostrar(fila[6]),
                    "Bloqueos recibidos": mostrar(fila[7]),
                    "% puntos": mostrar(fila[8], True),
                    "Eficiencia PDF": mostrar(fila[9], True),
                    "% excelente": mostrar(fila[10], True),
                    "% positivo": mostrar(fila[11], True),
                }

                detalle.append(registro)

            columnas_por_fundamento = {
                "Ataque": [
                    "Dorsal",
                    "Jugador",
                    "Posición",
                    "Acciones",
                    "Errores",
                    "Bloqueos recibidos",
                    "Puntos",
                    "% puntos",
                    "Eficiencia PDF",
                ],
                "Saque": [
                    "Dorsal",
                    "Jugador",
                    "Posición",
                    "Acciones",
                    "Errores",
                    "Puntos",
                ],
                "Recepción": [
                    "Dorsal",
                    "Jugador",
                    "Posición",
                    "Acciones",
                    "Errores",
                    "% excelente",
                    "% positivo",
                ],
                "Defensa": [
                    "Dorsal",
                    "Jugador",
                    "Posición",
                    "Acciones",
                    "Errores",
                    "% positivo",
                ],
                "Bloqueo": [
                    "Dorsal",
                    "Jugador",
                    "Posición",
                    "Errores",
                    "Puntos",
                ],
            }

            if fundamento_elegido in columnas_por_fundamento:
                columnas = columnas_por_fundamento[fundamento_elegido]

                detalle = [
                    {columna: registro[columna] for columna in columnas}
                    for registro in detalle
                ]

            st.dataframe(
                [
                    {
                        columna: str(valor) if valor is not None else "—"
                        for columna, valor in fila.items()
                    }
                    for fila in detalle
                ],
                width="stretch",
                hide_index=True,
                column_config={
                    "Jugador": st.column_config.TextColumn(
                        "Jugador",
                        width="large"
                    ),
                    "Posición": st.column_config.TextColumn(
                        "Posición",
                        width="medium"
                    ),
                }
            )

            st.divider()
            st.subheader("🏆 Producción de puntos")

            puntos_jugadores = {}

            for fila in individuales:
                dorsal, nombre, _, fundamento, _, _, puntos, *_ = fila

                if fundamento not in ("Ataque", "Saque", "Bloqueo"):
                    continue

                etiqueta = f"#{dorsal} {nombre}"

                puntos_jugadores[etiqueta] = (
                    puntos_jugadores.get(etiqueta, 0)
                    + (puntos or 0)
                )

            if puntos_jugadores:
                ranking = [
                    {"Jugador": jugador, "Puntos": puntos}
                    for jugador, puntos in puntos_jugadores.items()
                ]

                ranking.sort(
                    key=lambda fila: fila["Puntos"],
                    reverse=True
                )

                st.bar_chart(
                    ranking,
                    x="Jugador",
                    y="Puntos",
                    horizontal=True
                )
        else:
            st.info("Todavía no hay estadísticas individuales.")










    # CHV1995_ANALISIS_TECNICO_INDIVIDUAL_V1
    st.divider()
    st.subheader("🧠 Análisis técnico individual")

    with conectar() as conexion_evaluaciones:
        evaluaciones = conexion_evaluaciones.execute(
            """
            SELECT j.dorsal, j.nombre, e.observaciones
            FROM evaluaciones_jugador e
            JOIN jugadores j ON j.id = e.jugador_id
            WHERE e.partido_id = ?
            ORDER BY j.dorsal
            """,
            (partido_id,),
        ).fetchall()

    if evaluaciones:
        st.caption(
            "Observaciones técnicas orientadas al desarrollo individual "
            "y a la mejora colectiva."
        )

        for dorsal, nombre, observacion in evaluaciones:
            with st.expander(f"#{dorsal} · {nombre}"):
                st.write(observacion)
    else:
        st.info(
            "Todavía no hay evaluaciones técnicas registradas "
            "para este partido."
        )

# CHV1995_AJUSTE_BANNER_PANELES_V2
st.markdown("""
<style>
.st-key-chv-resumen-panel,
.st-key-chv-actividad-panel,
.st-key-chv-radar-panel {
    margin-top: -18px !important;
}
</style>
""", unsafe_allow_html=True)
