from html import escape
import pandas as pd
import streamlit as st


def mostrar_tabla_html(datos, ayudas=None):
    """Muestra una tabla centrada con el diseño de Volley Chamar."""
    tabla = pd.DataFrame(datos)

    if tabla.empty:
        st.info("No hay datos disponibles.")
        return

    ayudas = ayudas or {}

    encabezados = "".join(
        f'<th title="{escape(ayudas.get(str(columna), ""), quote=True)}">'
        f'{escape(str(columna))}</th>'
        for columna in tabla.columns
    )

    filas = ""
    for _, fila in tabla.iterrows():
        celdas = "".join(
            f"<td>{escape(str(valor)) if pd.notna(valor) else '—'}</td>"
            for valor in fila
        )
        filas += f"<tr>{celdas}</tr>"

    html = f"""
    <style>
    .chv-tabla-contenedor {{
        width: 100%;
        overflow-x: auto;
        border: 1px solid #30343d;
        border-radius: 10px;
        margin: 12px 0 20px;
    }}

    .chv-tabla {{
        width: 100%;
        border-collapse: collapse;
        background: #0e1016;
        color: #f5f5f5;
        font-size: 14px;
    }}

    .chv-tabla th {{
        background: #1a1d25;
        color: #c6c8d0;
        font-weight: 600;
        text-align: center;
        padding: 13px 12px;
        white-space: nowrap;
        border-bottom: 1px solid #30343d;
    }}

    .chv-tabla td {{
        text-align: center;
        padding: 12px;
        border-top: 1px solid #292d35;
    }}

    .chv-tabla th + th,
    .chv-tabla td + td {{
        border-left: 1px solid #292d35;
    }}

    .chv-tabla tbody tr:hover {{
        background: #242833;
    }}
    </style>

    <div class="chv-tabla-contenedor">
        <table class="chv-tabla">
            <thead><tr>{encabezados}</tr></thead>
            <tbody>{filas}</tbody>
        </table>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)
