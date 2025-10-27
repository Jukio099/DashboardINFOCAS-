"""
Módulo centralizado para la generación de gráficos con Plotly.
Versión 3.0 - Correcciones finales de estética y renderizado.
"""

import plotly.express as px
import plotly.graph_objects as go
from utils.loader import get_data_loader
import textwrap
import pandas as pd

# Paleta de colores para consistencia visual
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'text_dark': '#333333'
}

def create_generic_error_figure(message="No hay datos disponibles"):
    """Genera una figura de Plotly estándar para mostrar errores o datos vacíos."""
    fig = go.Figure()
    fig.update_layout(
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[{
            "text": message, "xref": "paper", "yref": "paper",
            "showarrow": False, "font": {"size": 16, "color": "grey"}
        }]
    )
    return fig

def create_sectores_chart_plotly():
    """Crea un Treemap de Sectores Económicos con Plotly."""
    df_raw = get_data_loader().get_sectores_economicos()
    if df_raw.empty:
        return create_generic_error_figure("Datos de Sectores No Disponibles")

    # Aislar y limpiar los datos específicos para este gráfico
    df = df_raw[['sector_econmico', 'participacin_porcentual']].copy()
    df['participacin_porcentual'] = pd.to_numeric(df['participacin_porcentual'], errors='coerce')
    df.dropna(subset=['participacin_porcentual'], inplace=True)
    df_filtered = df[~df['sector_econmico'].str.contains("Total", na=False)]

    if df_filtered.empty:
        return create_generic_error_figure("No hay datos válidos para el treemap")

    fig = px.treemap(
        df_filtered,
        path=[px.Constant("Todos los Sectores"), 'sector_econmico'],
        values='participacin_porcentual',
        color='participacin_porcentual',
        color_continuous_scale='Viridis',
        title="Participación de Sectores Económicos en el PIB"
    )
    fig.update_traces(textinfo="label+percent entry", textfont_size=14)
    fig.update_layout(height=400, font=dict(family="Inter, sans-serif"), margin=dict(t=50, r=10, b=10, l=10))
    return fig

def create_empresas_chart_plotly():
    """Crea un Gráfico de Dona de Distribución Empresarial con Plotly."""
    df = get_data_loader().get_empresas_por_tamano()
    if df.empty:
        return create_generic_error_figure()

    df_filtered = df[df['tamao_de_empresa'] != 'Total']

    fig = go.Figure(data=[go.Pie(
        labels=df_filtered['tamao_de_empresa'],
        values=df_filtered['nmero_de_empresas'],
        hole=.4,
        marker_colors=px.colors.qualitative.Pastel
    )])
    # Mover etiquetas afuera para mayor claridad
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.update_layout(
        height=400,
        font=dict(family="Inter, sans-serif"),
        title_text="Distribución de Empresas por Tamaño",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=50, r=10, b=10, l=10)
    )
    return fig

def create_graduados_chart_plotly():
    """Crea un Gráfico de Barras de Graduados con Plotly."""
    df = get_data_loader().get_graduados_por_area()
    if df.empty:
        return create_generic_error_figure()

    df_filtered = df[df['rea_de_conocimiento'] != 'Total']
    df_sorted = df_filtered.sort_values('nmero_de_graduados', ascending=True)

    df_sorted['rea_de_conocimiento'] = df_sorted['rea_de_conocimiento'].apply(
        lambda x: '<br>'.join(textwrap.wrap(x, width=30))
    )

    fig = go.Figure(go.Bar(
        y=df_sorted['rea_de_conocimiento'],
        x=df_sorted['nmero_de_graduados'],
        orientation='h',
        marker=dict(color=COLORS['primary']),
        text=df_sorted['nmero_de_graduados'],
        texttemplate='%{text:,.0f}',
        textposition='outside'
    ))
    fig.update_layout(
        height=500,
        xaxis_title="Número de Graduados",
        yaxis_title="",
        font=dict(family="Inter, sans-serif"),
        title_text="Capital Humano Formado por Área",
        margin=dict(t=50, r=10, b=10, l=250) # Aumentar margen izquierdo
    )
    return fig

def create_dengue_chart_plotly():
    """Crea un Gráfico de Líneas de Casos de Dengue con Plotly."""
    df = get_data_loader().get_dengue_data()
    if df.empty:
        return create_generic_error_figure()

    fig = go.Figure()
    for indicador in df['indicador'].unique():
        df_indicador = df[df['indicador'] == indicador]
        fig.add_trace(go.Scatter(
            x=df_indicador['ao'],
            y=df_indicador['valor'],
            mode='lines+markers',
            name=indicador
        ))

    fig.update_layout(
        height=400,
        xaxis_title="Año",
        yaxis_title="Número de Casos",
        font=dict(family="Inter, sans-serif"),
        title_text="Evolución de Casos de Dengue",
        legend_title_text='Tipo de Caso',
        margin=dict(t=50, r=10, b=10, l=10),
        xaxis = dict(
            tickmode = 'linear',
            tick0 = df['ao'].min(),
            dtick = 1
        )
    )
    return fig
