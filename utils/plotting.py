"""
Módulo de visualización para el Dashboard de Competitividad de Casanare
Versión 3.5 - Desactivar MaxRowsError para forzar el embebido de datos
"""

import altair as alt
import pandas as pd
from utils.loader import get_data_loader

# --- Configuración Global de Altair ---

# Desactiva el límite de filas, forzando a Altair a embeber los datos en el JSON
# en lugar de guardarlos en un archivo temporal. Este es el fix definitivo.
alt.data_transformers.disable_max_rows()

# Paleta de colores corporativa
PALETA_COLORES = {
    "principal": "#1f77b4",
    "secundario": "#ff7f0e",
    "verde": "#2ca02c",
    "rojo": "#d62728",
    "neutro": "#7f7f7f",
    "fondo": "#F5F5F5"
}

def altair_theme():
    """Configuración de tema global para Altair"""
    return {
        "config": {
            "title": {"fontSize": 18, "font": "Inter, sans-serif", "fontWeight": "bold", "anchor": "start", "color": "#333"},
            "axis": {"labelFont": "Inter, sans-serif", "labelFontSize": 12, "titleFont": "Inter, sans-serif", "titleFontSize": 14, "titleFontWeight": "normal", "gridColor": "#e0e0e0"},
            "legend": {"labelFont": "Inter, sans-serif", "labelFontSize": 12, "titleFont": "Inter, sans-serif", "titleFontSize": 14, "titleFontWeight": "normal"},
            "view": {"stroke": "transparent"},
            "background": PALETA_COLORES["fondo"]
        }
    }

alt.themes.register("casanare_theme", altair_theme)
alt.themes.enable("casanare_theme")

def chart_to_html(chart):
    """Convierte un gráfico de Altair a HTML con un template robusto."""
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
    """Genera un gráfico de marcador de posición como HTML"""
    chart = alt.Chart(pd.DataFrame()).mark_text(
        text=f"Gráfico '{title}' en desarrollo", size=20
    ).properties(width=500, height=400).configure_view(stroke=None)
    return chart_to_html(chart)

def create_sectores_chart():
    """Crea un treemap de los sectores económicos de Casanare."""
    data_loader = get_data_loader()
    df = data_loader.get_sectores_economicos()

    if df.empty or 'participacin_porcentual' not in df.columns or 'sector_econmico' not in df.columns:
        return create_placeholder_chart("Datos de Sectores No Disponibles")

    df['sector_econmico'] = df['sector_econmico'].astype(str)
    
    chart = alt.Chart(df).mark_treemap(stroke=PALETA_COLORES["fondo"], strokeWidth=2).encode(
        area=alt.Area('participacin_porcentual:Q', title="Participación (%)"),
        color=alt.Color('sector_econmico:N', legend=None, scale=alt.Scale(scheme='blues')),
        tooltip=[
            alt.Tooltip('sector_econmico:N', title="Sector"),
            alt.Tooltip('participacin_porcentual:Q', title="Participación", format=".2f"),
        ]
    ).properties(
        title={"text": "Composición del PIB de Casanare por Sector", "subtitle": "Áreas más grandes indican mayor contribución al PIB", "color": PALETA_COLORES["principal"], "subtitleColor": PALETA_COLORES["neutro"]},
        width=alt.Step(120), height=400
    ).configure_view(stroke='transparent')
    
    text = chart.mark_text(align='center', baseline='middle', color='white', fontSize=12, fontWeight='bold').encode(
        text='sector_econmico:N',
        opacity=alt.condition(alt.datum.participacin_porcentual > 2, alt.value(1), alt.value(0))
    )
    return chart_to_html(chart + text)

def create_empresas_chart():
    """Crea un gráfico de dona para la distribución de empresas por tamaño."""
    data_loader = get_data_loader()
    df = data_loader.get_empresas_por_tamano()

    if df.empty or 'nmero_de_empresas' not in df.columns or 'tamao_de_empresa' not in df.columns:
        return create_placeholder_chart("Datos de Empresas No Disponibles")

    chart = alt.Chart(df).mark_arc(innerRadius=90, outerRadius=120, cornerRadius=10).encode(
        theta=alt.Theta(field="nmero_de_empresas", type="quantitative", stack=True),
        color=alt.Color(field="tamao_de_empresa", type="nominal", legend=alt.Legend(title="Tamaño de Empresa", orient="right"), scale=alt.Scale(scheme='category10')),
        tooltip=[
            alt.Tooltip("tamao_de_empresa", title="Tamaño"),
            alt.Tooltip("nmero_de_empresas", title="Nº de Empresas", format=","),
            alt.Tooltip("porcentaje_del_total", title="Porcentaje", format=".2f"),
        ]
    ).properties(
        title={"text": "Distribución de Empresas por Tamaño", "subtitle": "Proporción de micro, pequeñas, medianas y grandes empresas", "color": PALETA_COLORES["principal"], "subtitleColor": PALETA_COLORES["neutro"]},
        height=400
    )
    return chart_to_html(chart)

def create_graduados_chart():
    """Crea un gráfico de barras horizontales de graduados por área de conocimiento."""
    data_loader = get_data_loader()
    df = data_loader.get_graduados_por_area()

    if df.empty or 'nmero_de_graduados' not in df.columns or 'rea_de_conocimiento' not in df.columns:
        return create_placeholder_chart("Datos de Graduados No Disponibles")

    df = df.sort_values('nmero_de_graduados', ascending=False)
    chart = alt.Chart(df).mark_bar(cornerRadius=5, height=25).encode(
        x=alt.X('nmero_de_graduados:Q', title='Número de Graduados'),
        y=alt.Y('rea_de_conocimiento:N', title='Área de Conocimiento', sort='-x'),
        color=alt.Color('rea_de_conocimiento:N', legend=None, scale=alt.Scale(scheme='viridis')),
        tooltip=[
            alt.Tooltip('rea_de_conocimiento:N', title='Área'),
            alt.Tooltip('nmero_de_graduados:Q', title='Nº de Graduados', format=','),
        ]
    ).properties(
        title={"text": "Capital Humano Formado por Área", "subtitle": "Número de graduados en programas de educación superior", "color": PALETA_COLORES["principal"], "subtitleColor": PALETA_COLORES["neutro"]},
        height=400
    )
    return chart_to_html(chart)

def create_dengue_chart():
    """Crea un gráfico de líneas para la evolución de casos de dengue."""
    data_loader = get_data_loader()
    df = data_loader.get_dengue_data()

    if df.empty or 'ao' not in df.columns or 'valor' not in df.columns or 'indicador' not in df.columns:
        return create_placeholder_chart("Datos de Dengue No Disponibles")

    df['ao'] = pd.to_datetime(df['ao'], format='%Y')
    df['indicador'] = df['indicador'].str.replace('CASOS DE', '').str.strip()
    chart = alt.Chart(df).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X('ao:T', title='Año', axis=alt.Axis(format='%Y')),
        y=alt.Y('valor:Q', title='Número de Casos'),
        color=alt.Color('indicador:N', legend=alt.Legend(title='Tipo de Caso', orient='bottom')),
        tooltip=[alt.Tooltip('ao:T', title='Año', format='%Y'), alt.Tooltip('indicador:N', title='Tipo'), alt.Tooltip('valor:Q', title='Casos', format=',')]
    ).properties(
        title={"text": "Evolución de Casos de Dengue", "subtitle": "Tendencia anual de los diferentes tipos de dengue reportados", "color": PALETA_COLORES["principal"], "subtitleColor": PALETA_COLORES["neutro"]},
        height=400
    ).interactive()
    return chart_to_html(chart)

# --- Funciones de Gráficos para otras páginas (placeholders) ---

def create_sectores_economico_chart():
    return create_placeholder_chart("Composición del PIB")

def create_cultivos_chart():
    return create_placeholder_chart("Brechas de Productividad")

def create_empresas_escala_chart():
    return create_placeholder_chart("Escala Empresarial")

def create_empresas_geo_chart():
    return create_placeholder_chart("Distribución Geográfica")

def create_graduados_educacion_chart():
    return create_placeholder_chart("Capital Humano Formado")

def create_desercion_chart():
    return create_placeholder_chart("Permanencia en el Sistema")

def create_salud_tendencias_chart():
    return create_placeholder_chart("Tendencias de Salud")

def create_seguridad_chart():
    return create_placeholder_chart("Incidencia de Delitos")