"""Visualizaciones centrales del Dashboard de Competitividad de Casanare."""

from __future__ import annotations

import re
from typing import Optional

import altair as alt
import pandas as pd

from utils.loader import get_data_loader

# --- Configuración Global de Altair ---------------------------------------------------------

alt.data_transformers.disable_max_rows()

PALETA_COLORES = {
    "principal": "#1f77b4",
    "secundario": "#ff7f0e",
    "verde": "#2ca02c",
    "rojo": "#d62728",
    "neutro": "#7f7f7f",
    "fondo": "#F5F5F5",
}


def altair_theme() -> dict:
    """Tema corporativo aplicado a todos los gráficos de Altair."""

    return {
        "config": {
            "title": {
                "fontSize": 18,
                "font": "Inter, sans-serif",
                "fontWeight": "bold",
                "anchor": "start",
                "color": "#333333",
            },
            "axis": {
                "labelFont": "Inter, sans-serif",
                "labelFontSize": 12,
                "titleFont": "Inter, sans-serif",
                "titleFontSize": 14,
                "titleFontWeight": "normal",
                "gridColor": "#e0e0e0",
            },
            "legend": {
                "labelFont": "Inter, sans-serif",
                "labelFontSize": 12,
                "titleFont": "Inter, sans-serif",
                "titleFontSize": 14,
                "titleFontWeight": "normal",
            },
            "view": {"stroke": "transparent"},
            "background": PALETA_COLORES["fondo"],
        }
    }


alt.themes.register("casanare_theme", altair_theme)
alt.themes.enable("casanare_theme")


# --- Utilidades -----------------------------------------------------------------------------

def chart_to_html(chart: alt.Chart) -> str:
    """Convierte un gráfico de Altair a HTML listo para embeber en un iframe."""

    chart_json = chart.to_json(indent=None)
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
      <script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
      <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
    </head>
    <body>
      <div id="vis"></div>
      <script type="text/javascript">
        const spec = {chart_json};
        vegaEmbed('#vis', spec, {{"actions": false}}).catch(console.error);
      </script>
    </body>
    </html>
    """


def create_placeholder_chart(title: str) -> str:
    """Crea un gráfico de marcador de posición cuando faltan datos."""

    chart = (
        alt.Chart(pd.DataFrame({"mensaje": [f"Gráfico '{title}' en desarrollo"]}))
        .mark_text(text=f"Gráfico '{title}' en desarrollo", size=18, color="#757575")
        .properties(width=520, height=360)
    )
    return chart_to_html(chart)


def _extract_number(value: object, *, allow_zero: bool = False) -> Optional[float]:
    """Obtiene el primer número significativo de un string.

    Se ignoran fechas y horas que provienen de celdas mal tipadas en Excel.
    """

    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None

    text = str(value).strip()
    if not text:
        return None
    if "00:00:00" in text and re.search(r"\d{4}-\d{2}-\d{2}", text):
        return None

    text = text.replace(",", ".")
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    if not match:
        return None

    number = float(match.group())
    if not allow_zero and number == 0:
        return None
    return number


def _extract_percentage(value: object) -> Optional[float]:
    """Normaliza valores porcentuales expresados como strings."""

    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None

    text = str(value).strip()
    if not text:
        return None
    if "00:00:00" in text and re.search(r"\d{4}-\d{2}-\d{2}", text):
        return None

    text = text.replace(",", ".")
    numbers = re.findall(r"-?\d+(?:\.\d+)?", text)
    if not numbers:
        return None

    values = [float(n) for n in numbers]
    if "-" in text and len(values) >= 2:
        number = sum(values) / len(values)
    else:
        number = values[0]

    if number <= 1:
        number *= 100
    return number


def _format_measure(value: Optional[float], *, suffix: str = "", decimals: int = 1) -> str:
    """Formatea números para tooltips amigables."""

    if value is None:
        return "Dato no disponible"
    if suffix == "%":
        return f"{value:.{decimals}f}%"
    return f"{value:,.{decimals}f}{suffix}"


# --- Gráficos de la página principal --------------------------------------------------------

def create_sectores_chart() -> str:
    """Treemap (implementado como rectángulos apilados) del peso sectorial."""

    data_loader = get_data_loader()
    df = data_loader.get_sectores_economicos().copy()
    if df.empty:
        return create_placeholder_chart("Sectores económicos")

    df = df[~df["sector_econmico"].str.contains("Total", case=False, na=False)]
    df["participacin_porcentual"] = pd.to_numeric(df["participacin_porcentual"], errors="coerce")
    df = df.dropna(subset=["participacin_porcentual"])

    base = alt.Chart(df).mark_rect().encode(
        x=alt.X("sum(participacin_porcentual):Q", stack="normalize", axis=None),
        y=alt.Y("sector_econmico:N", title="Sector", sort="-x"),
        color=alt.Color(
            "sector_econmico:N",
            scale=alt.Scale(scheme="blues"),
            legend=None,
        ),
        tooltip=[
            alt.Tooltip("sector_econmico:N", title="Sector"),
            alt.Tooltip("participacin_porcentual:Q", title="Participación", format=".1f"),
        ],
    ).properties(
        title={
            "text": "Composición del PIB por sector",
            "subtitle": "Participación porcentual en el PIB departamental",
            "color": PALETA_COLORES["principal"],
            "subtitleColor": PALETA_COLORES["neutro"],
        },
        height=360,
    )

    text = base.mark_text(align="left", dx=4, color="#FFFFFF", fontWeight="bold").encode(
        text=alt.Text("sector_econmico:N"),
        opacity=alt.condition(alt.datum.participacin_porcentual > 3, alt.value(1), alt.value(0)),
    )

    return chart_to_html(base + text)


def create_empresas_chart() -> str:
    """Dona que resume la estructura empresarial por tamaño."""

    data_loader = get_data_loader()
    df = data_loader.get_empresas_por_tamano().copy()
    if df.empty:
        return create_placeholder_chart("Empresas por tamaño")

    df = df[df["tamao_de_empresa"] != "Total"]
    df["nmero_de_empresas"] = pd.to_numeric(df["nmero_de_empresas"], errors="coerce")
    df["porcentaje_del_total"] = df["porcentaje_del_total"].apply(_extract_percentage)
    df = df.dropna(subset=["nmero_de_empresas"])

    chart = alt.Chart(df).mark_arc(innerRadius=90, outerRadius=130, cornerRadius=8).encode(
        theta=alt.Theta("nmero_de_empresas:Q", stack=True),
        color=alt.Color(
            "tamao_de_empresa:N",
            title="Tamaño de empresa",
            scale=alt.Scale(scheme="category10"),
        ),
        tooltip=[
            alt.Tooltip("tamao_de_empresa:N", title="Tamaño"),
            alt.Tooltip("nmero_de_empresas:Q", title="Empresas", format=","),
            alt.Tooltip("porcentaje_del_total:Q", title="Participación", format=".1f"),
        ],
    ).properties(
        title={
            "text": "Distribución de empresas por tamaño",
            "subtitle": "Composición del tejido productivo formal",
            "color": PALETA_COLORES["principal"],
            "subtitleColor": PALETA_COLORES["neutro"],
        },
        height=420,
    )

    return chart_to_html(chart)


def create_graduados_chart() -> str:
    """Barras horizontales que muestran el capital humano formado."""

    data_loader = get_data_loader()
    df = data_loader.get_graduados_por_area().copy()
    if df.empty:
        return create_placeholder_chart("Graduados")

    df = df[df["rea_de_conocimiento"] != "Total"]
    df = df.sort_values("nmero_de_graduados", ascending=False)

    chart = alt.Chart(df).mark_bar(cornerRadius=6, height=28).encode(
        x=alt.X("nmero_de_graduados:Q", title="Número de graduados"),
        y=alt.Y("rea_de_conocimiento:N", title="Área de conocimiento", sort="-x"),
        color=alt.Color("rea_de_conocimiento:N", legend=None, scale=alt.Scale(scheme="viridis")),
        tooltip=[
            alt.Tooltip("rea_de_conocimiento:N", title="Área"),
            alt.Tooltip("nmero_de_graduados:Q", title="Graduados", format=","),
            alt.Tooltip("porcentaje_del_total:Q", title="Participación", format=".1%")
        ],
    ).properties(
        title={
            "text": "Graduados por área de conocimiento",
            "subtitle": "Participación en el total de titulados recientes",
            "color": PALETA_COLORES["principal"],
            "subtitleColor": PALETA_COLORES["neutro"],
        },
        height=420,
    )

    return chart_to_html(chart)


def create_dengue_chart() -> str:
    """Evolución temporal de los casos de dengue en Casanare."""

    data_loader = get_data_loader()
    df = data_loader.get_dengue_data().copy()
    if df.empty:
        return create_placeholder_chart("Casos de dengue")

    df["ao"] = pd.to_datetime(df["ao"], format="%Y", errors="coerce")
    df = df.dropna(subset=["ao", "valor"])
    df["indicador"] = df["indicador"].str.replace("CASOS DE", "", case=False).str.strip().str.title()

    chart = alt.Chart(df).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X("ao:T", title="Año", axis=alt.Axis(format="%Y")),
        y=alt.Y("valor:Q", title="Casos reportados"),
        color=alt.Color("indicador:N", title="Tipo de reporte", legend=alt.Legend(orient="bottom")),
        tooltip=[
            alt.Tooltip("ao:T", title="Año", format="%Y"),
            alt.Tooltip("indicador:N", title="Tipo"),
            alt.Tooltip("valor:Q", title="Casos", format=","),
        ],
    ).properties(
        title={
            "text": "Evolución anual de los casos de dengue",
            "subtitle": "Seguimiento de la notificación epidemiológica",
            "color": PALETA_COLORES["principal"],
            "subtitleColor": PALETA_COLORES["neutro"],
        },
        height=380,
    ).interactive()

    return chart_to_html(chart)


# --- Gráficos para las páginas temáticas ----------------------------------------------------

def create_sectores_economico_chart() -> str:
    """Ranking de participación sectorial en el PIB."""

    data_loader = get_data_loader()
    df = data_loader.get_sectores_economicos().copy()
    if df.empty:
        return create_placeholder_chart("Composición del PIB")

    df = df[~df["sector_econmico"].str.contains("Total", case=False, na=False)]
    df["participacin_porcentual"] = pd.to_numeric(df["participacin_porcentual"], errors="coerce")
    df = df.dropna(subset=["participacin_porcentual"])
    df = df.sort_values("participacin_porcentual", ascending=False)

    highlight = alt.selection_single(fields=["sector_econmico"], empty="none", on="mouseover")

    barras = alt.Chart(df).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6).encode(
        y=alt.Y("sector_econmico:N", title="Sector", sort=df["participacin_porcentual"].tolist()),
        x=alt.X("participacin_porcentual:Q", title="Participación en el PIB (%)"),
        color=alt.condition(highlight, alt.value(PALETA_COLORES["principal"]), alt.value("#90caf9")),
        tooltip=[
            alt.Tooltip("sector_econmico:N", title="Sector"),
            alt.Tooltip("participacin_porcentual:Q", title="Participación", format=".1f"),
        ],
    ).add_params(highlight)

    texto = barras.mark_text(align="left", dx=4, fontWeight="bold", color="#0d47a1").encode(
        text=alt.Text("participacin_porcentual:Q", format=".1f")
    )

    chart = (barras + texto).properties(
        title={
            "text": "Sectores con mayor aporte al PIB",
            "subtitle": "La barra azul indica los sectores líderes en la economía departamental",
            "color": PALETA_COLORES["principal"],
            "subtitleColor": PALETA_COLORES["neutro"],
        },
        height=420,
    )

    return chart_to_html(chart)


def create_cultivos_chart() -> str:
    """Brechas de productividad en cadenas agropecuarias estratégicas."""

    data_loader = get_data_loader()
    df = data_loader.get_cultivos_data().copy()
    if df.empty:
        return create_placeholder_chart("Brechas de productividad")

    columnas = [
        "sector",
        "criterio",
        "valor_actual_en_casanare",
        "escenario_ideal",
        "brecha_de_mejora_potencial",
    ]
    df = df[columnas]
    df["brecha_pct"] = df["brecha_de_mejora_potencial"].apply(_extract_percentage)
    df["valor_actual"] = df.apply(
        lambda fila: _extract_percentage(fila["valor_actual_en_casanare"]) if "%" in str(fila["criterio"]).lower() else _extract_number(fila["valor_actual_en_casanare"], allow_zero=True),
        axis=1,
    )
    df["valor_ideal"] = df.apply(
        lambda fila: _extract_percentage(fila["escenario_ideal"]) if "%" in str(fila["criterio"]).lower() else _extract_number(fila["escenario_ideal"], allow_zero=True),
        axis=1,
    )

    df = df.dropna(subset=["sector", "brecha_pct"])
    df = df.sort_values("brecha_pct", ascending=False)
    df["brecha_pct"] = df["brecha_pct"].clip(0, 100)

    df["valor_actual_texto"] = df.apply(
        lambda fila: _format_measure(fila["valor_actual"], suffix="%" if "%" in str(fila["criterio"]).lower() else "", decimals=1),
        axis=1,
    )
    df["valor_ideal_texto"] = df.apply(
        lambda fila: _format_measure(fila["valor_ideal"], suffix="%" if "%" in str(fila["criterio"]).lower() else "", decimals=1),
        axis=1,
    )

    chart = alt.Chart(df).mark_bar(cornerRadius=6).encode(
        x=alt.X("brecha_pct:Q", title="Brecha de mejora (%)"),
        y=alt.Y("sector:N", title="Cadena productiva", sort=df["brecha_pct"].tolist()),
        color=alt.Color("brecha_pct:Q", scale=alt.Scale(scheme="oranges"), legend=None),
        tooltip=[
            alt.Tooltip("sector:N", title="Cadena"),
            alt.Tooltip("criterio:N", title="Indicador evaluado"),
            alt.Tooltip("brecha_pct:Q", title="Brecha", format=".1f"),
            alt.Tooltip("valor_actual_texto:N", title="Valor actual"),
            alt.Tooltip("valor_ideal_texto:N", title="Escenario ideal"),
        ],
    ).properties(
        title={
            "text": "Prioridades para cerrar brechas de productividad agropecuaria",
            "subtitle": "Porcentaje que separa la situación actual del escenario meta",
            "color": PALETA_COLORES["principal"],
            "subtitleColor": PALETA_COLORES["neutro"],
        },
        height=400,
    )

    return chart_to_html(chart)


def create_empresas_escala_chart() -> str:
    """Detalle de empresas por tamaño y participación."""

    data_loader = get_data_loader()
    df = data_loader.get_empresas_por_tamano().copy()
    if df.empty:
        return create_placeholder_chart("Escala empresarial")

    df = df[df["tamao_de_empresa"] != "Total"]
    df["nmero_de_empresas"] = pd.to_numeric(df["nmero_de_empresas"], errors="coerce")
    df["porcentaje_del_total"] = df["porcentaje_del_total"].apply(_extract_percentage)
    df = df.dropna(subset=["nmero_de_empresas"])
    df = df.sort_values("nmero_de_empresas", ascending=True)

    barras = alt.Chart(df).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6).encode(
        y=alt.Y("tamao_de_empresa:N", title="Tamaño", sort=df["nmero_de_empresas"].tolist()),
        x=alt.X("nmero_de_empresas:Q", title="Número de empresas"),
        color=alt.Color("porcentaje_del_total:Q", title="% del total", scale=alt.Scale(scheme="blues")),
        tooltip=[
            alt.Tooltip("tamao_de_empresa:N", title="Tamaño"),
            alt.Tooltip("nmero_de_empresas:Q", title="Empresas", format=","),
            alt.Tooltip("porcentaje_del_total:Q", title="Participación", format=".1f"),
        ],
    )

    texto = barras.mark_text(align="left", dx=4, color="#0d47a1", fontWeight="bold").encode(
        text=alt.Text("nmero_de_empresas:Q", format=",")
    )

    chart = (barras + texto).properties(
        title={
            "text": "Composición del tejido empresarial",
            "subtitle": "Predomina la microempresa, seguida de unidades pequeñas y medianas",
            "color": PALETA_COLORES["principal"],
            "subtitleColor": PALETA_COLORES["neutro"],
        },
        height=360,
    )

    return chart_to_html(chart)


def create_empresas_geo_chart() -> str:
    """Top de municipios por concentración empresarial."""

    data_loader = get_data_loader()
    df = data_loader.get_municipios_empresas().copy()
    if df.empty:
        return create_placeholder_chart("Distribución geográfica")

    df["nmero_de_empresas"] = pd.to_numeric(df["nmero_de_empresas"], errors="coerce")
    df["porcentaje_del_total"] = df["porcentaje_del_total"].apply(_extract_percentage)
    df = df.dropna(subset=["nmero_de_empresas"])
    df = df.sort_values("nmero_de_empresas", ascending=False).head(10)

    chart = alt.Chart(df).mark_bar(cornerRadius=6).encode(
        x=alt.X("nmero_de_empresas:Q", title="Número de empresas"),
        y=alt.Y("municipio:N", title="Municipio", sort="-x"),
        color=alt.Color("porcentaje_del_total:Q", title="% del total", scale=alt.Scale(scheme="greens")),
        tooltip=[
            alt.Tooltip("municipio:N", title="Municipio"),
            alt.Tooltip("nmero_de_empresas:Q", title="Empresas", format=","),
            alt.Tooltip("porcentaje_del_total:Q", title="Participación", format=".1f"),
        ],
    ).properties(
        title={
            "text": "Municipios con mayor presencia empresarial",
            "subtitle": "El top 10 concentra la mayor parte de compañías formales",
            "color": PALETA_COLORES["principal"],
            "subtitleColor": PALETA_COLORES["neutro"],
        },
        height=380,
    )

    return chart_to_html(chart)


def create_graduados_educacion_chart() -> str:
    """Análisis de graduados para la página de Educación."""

    data_loader = get_data_loader()
    df = data_loader.get_graduados_por_area().copy()
    if df.empty:
        return create_placeholder_chart("Capital humano")

    df = df[df["rea_de_conocimiento"] != "Total"]
    df = df.sort_values("nmero_de_graduados", ascending=False)

    chart = alt.Chart(df).mark_bar(cornerRadius=6, height=26).encode(
        x=alt.X("nmero_de_graduados:Q", title="Número de graduados"),
        y=alt.Y("rea_de_conocimiento:N", title="Área de conocimiento", sort="-x"),
        color=alt.Color("porcentaje_del_total:Q", title="% del total", scale=alt.Scale(scheme="purples")),
        tooltip=[
            alt.Tooltip("rea_de_conocimiento:N", title="Área"),
            alt.Tooltip("nmero_de_graduados:Q", title="Graduados", format=","),
            alt.Tooltip("porcentaje_del_total:Q", title="Participación", format=".1%"),
        ],
    ).properties(
        title={
            "text": "Oferta de talento profesional por área",
            "subtitle": "La intensidad del color refleja la participación en el total de títulos",
            "color": PALETA_COLORES["principal"],
            "subtitleColor": PALETA_COLORES["neutro"],
        },
        height=420,
    )

    return chart_to_html(chart)


def create_desercion_chart() -> str:
    """Evolución de la deserción escolar en los municipios priorizados."""

    data_loader = get_data_loader()
    df = data_loader.get_desercion_data().copy()
    if df.empty:
        return create_placeholder_chart("Permanencia en el sistema")

    df["tasa_desercin_pct"] = df["tasa_desercin"].apply(_extract_percentage)
    df["ao"] = pd.to_numeric(df["ao"], errors="coerce")
    df = df.dropna(subset=["tasa_desercin_pct", "ao"])

    promedio = df.groupby("municipio")["tasa_desercin_pct"].mean().sort_values(ascending=False)
    municipios_top = promedio.head(5).index.tolist()
    df_top = df[df["municipio"].isin(municipios_top)]

    chart = alt.Chart(df_top).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X("ao:O", title="Año"),
        y=alt.Y("tasa_desercin_pct:Q", title="Tasa de deserción (%)"),
        color=alt.Color("municipio:N", title="Municipio", legend=alt.Legend(orient="bottom")),
        tooltip=[
            alt.Tooltip("municipio:N", title="Municipio"),
            alt.Tooltip("ao:O", title="Año"),
            alt.Tooltip("tasa_desercin_pct:Q", title="Tasa", format=".2f"),
        ],
    ).properties(
        title={
            "text": "Municipios con mayores desafíos en permanencia escolar",
            "subtitle": "Comparativo 2019-2024: la meta es reducir la deserción",
            "color": PALETA_COLORES["principal"],
            "subtitleColor": PALETA_COLORES["neutro"],
        },
        height=420,
    ).interactive()

    return chart_to_html(chart)


def create_salud_tendencias_chart() -> str:
    """Serie histórica de los principales indicadores de mortalidad."""

    data_loader = get_data_loader()
    df = data_loader.get_mortalidad_data().copy()
    if df.empty:
        return create_placeholder_chart("Tendencias de salud")

    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["ao"] = pd.to_numeric(df["ao"], errors="coerce")
    df = df.dropna(subset=["valor", "ao"])

    top_indicadores = df.groupby("indicador")["valor"].mean().sort_values(ascending=False).head(3).index
    df_top = df[df["indicador"].isin(top_indicadores)]

    chart = alt.Chart(df_top).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X("ao:O", title="Año"),
        y=alt.Y("valor:Q", title="Tasa por 100.000 habitantes"),
        color=alt.Color("indicador:N", title="Indicador", legend=alt.Legend(orient="bottom")),
        tooltip=[
            alt.Tooltip("indicador:N", title="Indicador"),
            alt.Tooltip("ao:O", title="Año"),
            alt.Tooltip("valor:Q", title="Tasa", format=".2f"),
        ],
    ).properties(
        title={
            "text": "Tendencias de mortalidad en salud pública",
            "subtitle": "Indicadores priorizados según su incidencia reciente",
            "color": PALETA_COLORES["principal"],
            "subtitleColor": PALETA_COLORES["neutro"],
        },
        height=420,
    ).interactive()

    return chart_to_html(chart)


def create_seguridad_chart() -> str:
    """Comparativo de hechos que afectan la convivencia ciudadana."""

    data_loader = get_data_loader()
    df = data_loader.get_seguridad_data().copy()
    if df.empty:
        return create_placeholder_chart("Indicadores de seguridad")

    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["ao"] = pd.to_numeric(df["ao"], errors="coerce")
    df = df.dropna(subset=["valor", "ao"])

    max_year = df["ao"].max()
    top_indicadores = (
        df[df["ao"] == max_year]
        .sort_values("valor", ascending=False)
        ["indicador"]
        .head(6)
        .tolist()
    )
    df_top = df[df["indicador"].isin(top_indicadores)]

    chart = alt.Chart(df_top).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X("ao:O", title="Año"),
        y=alt.Y("valor:Q", title="Casos reportados"),
        color=alt.Color("indicador:N", title="Indicador", legend=alt.Legend(orient="bottom")),
        tooltip=[
            alt.Tooltip("indicador:N", title="Indicador"),
            alt.Tooltip("ao:O", title="Año"),
            alt.Tooltip("valor:Q", title="Casos", format=","),
        ],
    ).properties(
        title={
            "text": "Seguridad ciudadana: evolución de hechos relevantes",
            "subtitle": "Comparativo interanual de los principales indicadores 2024-2025",
            "color": PALETA_COLORES["principal"],
            "subtitleColor": PALETA_COLORES["neutro"],
        },
        height=420,
    ).interactive()

    return chart_to_html(chart)
