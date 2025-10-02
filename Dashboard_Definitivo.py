"""
Dashboard de Competitividad de Casanare - VERSIÓN DEFINITIVA
Con mapeo exacto de columnas y una gráfica por fila
"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
import logging
import numpy as np

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🏗️ FUNCIONES DE CARGA DE DATOS CON NOMBRES EXACTOS
def load_csv_data(filename: str) -> pd.DataFrame:
    """Carga datos CSV con nombres de columnas exactos."""
    try:
        file_path = Path("data/clean") / filename
        if not file_path.exists():
            logger.warning(f"Archivo no encontrado: {file_path}")
            return pd.DataFrame()
        
        df = pd.read_csv(file_path)
        df = df.dropna(how='all')
        
        logger.info(f"Datos cargados: {filename} - {len(df)} registros")
        logger.info(f"Columnas disponibles: {list(df.columns)}")
        return df
        
    except Exception as e:
        logger.error(f"Error cargando {filename}: {e}")
        return pd.DataFrame()

def get_kpi_values():
    """Extrae KPIs con nombres de columnas exactos."""
    df_general = load_csv_data("generalidades.csv")
    
    if df_general.empty:
        logger.warning("No se pudieron cargar los datos generales")
        return {}
    
    kpis = {}
    try:
        for _, row in df_general.iterrows():
            indicador = str(row.get('indicador', '')).lower()
            valor = row.get('valor', 0)
            
            if 'población' in indicador and 'total' in indicador:
                kpis['poblacion_2025'] = int(valor) if pd.notna(valor) else 0
            elif 'pib' in indicador and 'departamental' in indicador:
                kpis['pib_2023'] = float(valor) if pd.notna(valor) else 0
            elif 'puntaje' in indicador and 'general' in indicador:
                kpis['puntaje_idc'] = float(valor) if pd.notna(valor) else 0
            elif 'ranking' in indicador:
                ranking_val = row.get('rankingnacional2025', 0)
                kpis['ranking_idc'] = int(ranking_val) if pd.notna(ranking_val) else 0
    except Exception as e:
        logger.error(f"Error procesando datos generales para KPIs: {e}")
        return {}
    
    return kpis

def get_empresas_total():
    """Calcula el total de empresas con nombre de columna exacto."""
    df_empresas = load_csv_data("empresarial.csv")
    if df_empresas.empty:
        return 0
    
    try:
        # Usar el nombre exacto de la columna
        total = df_empresas['numero_de_empresas'].sum()
        return int(total) if pd.notna(total) else 0
    except Exception as e:
        logger.error(f"Error calculando total de empresas: {e}")
        return 0

# 🎨 FUNCIONES DE VISUALIZACIÓN CON NOMBRES EXACTOS

def create_treemap_sectores(df_sectores: pd.DataFrame) -> go.Figure:
    """Crea treemap con nombres de columnas exactos."""
    if df_sectores.empty:
        return go.Figure().add_annotation(text="No hay datos disponibles", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Usar nombres exactos de columnas
    df_clean = df_sectores.copy()
    
    # Verificar que las columnas existen
    if 'participacion_porcentual' not in df_clean.columns:
        logger.error(f"Columna 'participacion_porcentual' no encontrada. Columnas disponibles: {list(df_clean.columns)}")
        return go.Figure().add_annotation(text="Error: Columna no encontrada", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    df_clean = df_clean[
        (df_clean['participacion_porcentual'].notna()) &
        (df_clean['participacion_porcentual'] > 0)
    ].copy()
    
    if df_clean.empty:
        return go.Figure().add_annotation(text="No hay datos válidos", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Crear treemap
    fig = px.treemap(
        df_clean,
        path=['sector_economico'],
        values='participacion_porcentual',
        title="<b>Composición del PIB por Sectores Económicos</b>",
        color='participacion_porcentual',
        color_continuous_scale='Viridis'
    )
    
    fig.update_traces(
        textinfo="label+percent entry",
        textfont_size=14,
        textfont_color='white'
    )
    
    fig.update_layout(
        height=500,
        font=dict(family="Inter, Arial, sans-serif", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_funnel_empresas(df_empresas: pd.DataFrame) -> go.Figure:
    """Crea funnel con nombres de columnas exactos."""
    if df_empresas.empty:
        return go.Figure().add_annotation(text="No hay datos disponibles", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Verificar columnas
    if 'numero_de_empresas' not in df_empresas.columns:
        logger.error(f"Columna 'numero_de_empresas' no encontrada. Columnas disponibles: {list(df_empresas.columns)}")
        return go.Figure().add_annotation(text="Error: Columna no encontrada", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    df_clean = df_empresas[df_empresas['numero_de_empresas'].notna()].copy()
    
    if df_clean.empty:
        return go.Figure().add_annotation(text="No hay datos válidos", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Crear funnel chart
    fig = go.Figure(go.Funnel(
        y=df_clean['tamano_de_empresa'],
        x=df_clean['numero_de_empresas'],
        textinfo="value+percent initial",
        marker=dict(color=['#FF7F0E', '#1f77b4', '#2ca02c', '#d62728', '#9467bd'])
    ))
    
    fig.update_layout(
        title="<b>Distribución del Tejido Empresarial por Tamaño</b>",
        height=500,
        font=dict(family="Inter, Arial, sans-serif", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_bar_graduados(df_graduados: pd.DataFrame) -> go.Figure:
    """Crea barras con nombres de columnas exactos."""
    if df_graduados.empty:
        return go.Figure().add_annotation(text="No hay datos disponibles", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Verificar columnas
    if 'número_de_graduados' not in df_graduados.columns:
        logger.error(f"Columna 'número_de_graduados' no encontrada. Columnas disponibles: {list(df_graduados.columns)}")
        return go.Figure().add_annotation(text="Error: Columna no encontrada", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    df_clean = df_graduados[df_graduados['número_de_graduados'].notna()].copy()
    df_clean = df_clean.sort_values('número_de_graduados', ascending=True)
    
    if df_clean.empty:
        return go.Figure().add_annotation(text="No hay datos válidos", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Crear gráfico de barras horizontales
    fig = go.Figure()
    
    colors = ['#FF7F0E' if i == len(df_clean)-1 else '#1f77b4' for i in range(len(df_clean))]
    
    fig.add_trace(go.Bar(
        y=df_clean['área_de_conocimiento'],
        x=df_clean['número_de_graduados'],
        orientation='h',
        marker=dict(color=colors),
        text=[f"{val:,.0f}" for val in df_clean['número_de_graduados']],
        textposition='outside',
        textfont=dict(size=11, color='#333333'),
        hovertemplate="<b>%{y}</b><br>" +
                     "Graduados: %{x:,.0f}<br>" +
                     "<extra></extra>",
        showlegend=False
    ))
    
    fig.update_layout(
        title="<b>Graduados por Área de Conocimiento</b>",
        xaxis_title="Número de Graduados",
        yaxis_title="",
        height=500,
        font=dict(family="Inter, Arial, sans-serif", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_line_dengue(df_morbilidad: pd.DataFrame) -> go.Figure:
    """Crea líneas con nombres de columnas exactos."""
    if df_morbilidad.empty:
        return go.Figure().add_annotation(text="No hay datos disponibles", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Verificar columnas
    if 'a_o' not in df_morbilidad.columns:
        logger.error(f"Columna 'a_o' no encontrada. Columnas disponibles: {list(df_morbilidad.columns)}")
        return go.Figure().add_annotation(text="Error: Columna año no encontrada", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Filtrar datos de dengue
    try:
        df_morbilidad['indicador'] = df_morbilidad['indicador'].astype(str)
        df_dengue = df_morbilidad[df_morbilidad['indicador'].str.contains('Dengue', case=False, na=False)]
    except Exception as e:
        logger.error(f"Error filtrando datos de dengue: {e}")
        return go.Figure().add_annotation(text="Error procesando datos", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    if df_dengue.empty:
        return go.Figure().add_annotation(text="No hay datos de dengue", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Crear gráfico de líneas usando 'a_o' como año
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_dengue['a_o'],
        y=df_dengue['valor'],
        mode='lines+markers',
        name='Casos de Dengue',
        line=dict(color='#FF7F0E', width=3),
        marker=dict(size=8),
        hovertemplate="<b>Año: %{x}</b><br>" +
                     "Casos: %{y:,.0f}<br>" +
                     "<extra></extra>"
    ))
    
    fig.update_layout(
        title="<b>Evolución de Casos de Dengue en Casanare</b>",
        xaxis_title="Año",
        yaxis_title="Número de Casos",
        height=500,
        font=dict(family="Inter, Arial, sans-serif", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

# Inicializar la aplicación Dash
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    ],
    suppress_callback_exceptions=True
)

app.title = "🏛️ Dashboard de Competitividad de Casanare"

# 🏛️ LAYOUT PRINCIPAL - UNA GRÁFICA POR FILA
app.layout = dbc.Container([
    html.H1("🏛️ Dashboard de Competitividad de Casanare", 
           style={'color': '#1f77b4', 'marginBottom': '2rem', 'textAlign': 'center'}),
    
    # KPIs Principales
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("👥 Población", className="text-center"),
                    html.H2(id="kpi-poblacion", className="text-center", 
                            style={'color': '#1f77b4', 'fontSize': '2.5rem'})
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("💰 PIB", className="text-center"),
                    html.H2(id="kpi-pib", className="text-center", 
                            style={'color': '#1f77b4', 'fontSize': '2.5rem'})
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("🏢 Empresas", className="text-center"),
                    html.H2(id="kpi-empresas", className="text-center", 
                            style={'color': '#1f77b4', 'fontSize': '2.5rem'})
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("🏆 Ranking", className="text-center"),
                    html.H2(id="kpi-ranking", className="text-center", 
                            style={'color': '#1f77b4', 'fontSize': '2.5rem'})
                ])
            ])
        ], width=3)
    ], className="mb-4"),
    
    # GRÁFICA 1: Sectores Económicos (UNA GRÁFICA POR FILA)
    dbc.Row([
        dbc.Col([
            html.H3("📊 Sectores Económicos", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
            dcc.Graph(id="grafico-sectores")
        ], width=12)
    ], className="mb-4"),
    
    # GRÁFICA 2: Empresas por Tamaño (UNA GRÁFICA POR FILA)
    dbc.Row([
        dbc.Col([
            html.H3("🏢 Distribución Empresarial", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
            dcc.Graph(id="grafico-empresas")
        ], width=12)
    ], className="mb-4"),
    
    # GRÁFICA 3: Graduados (UNA GRÁFICA POR FILA)
    dbc.Row([
        dbc.Col([
            html.H3("🎓 Graduados por Área de Conocimiento", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
            dcc.Graph(id="grafico-graduados")
        ], width=12)
    ], className="mb-4"),
    
    # GRÁFICA 4: Salud - Dengue (UNA GRÁFICA POR FILA)
    dbc.Row([
        dbc.Col([
            html.H3("🩺 Evolución de Casos de Dengue", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
            dcc.Graph(id="grafico-dengue")
        ], width=12)
    ], className="mb-4")
    
], fluid=True)

# 🔄 CALLBACKS
@app.callback(
    [Output("kpi-poblacion", "children"),
     Output("kpi-pib", "children"),
     Output("kpi-empresas", "children"),
     Output("kpi-ranking", "children")],
    [Input("kpi-poblacion", "id")]
)
def update_kpis(_):
    try:
        kpis = get_kpi_values()
        empresas_totales = get_empresas_total()
        
        poblacion = kpis.get('poblacion_2025', 0)
        pib = kpis.get('pib_2023', 0)
        ranking = kpis.get('ranking_idc', 0)
        
        poblacion_str = f"{poblacion:,}" if poblacion > 0 else "N/A"
        pib_billones = pib / 1000000 if pib > 0 else 0
        pib_str = f"${pib_billones:.1f}B" if pib_billones > 0 else "N/A"
        empresas_str = f"{empresas_totales:,}" if empresas_totales > 0 else "N/A"
        ranking_str = f"#{ranking}" if ranking > 0 else "N/A"
        
        logger.info(f"KPIs: Población={poblacion_str}, PIB={pib_str}, Empresas={empresas_str}, Ranking={ranking_str}")
        
        return poblacion_str, pib_str, empresas_str, ranking_str
        
    except Exception as e:
        logger.error(f"Error actualizando KPIs: {e}")
        return "Error", "Error", "Error", "Error"

@app.callback(Output("grafico-sectores", "figure"), [Input("grafico-sectores", "id")])
def update_sectores(_):
    df_sectores = load_csv_data("sector_economico.csv")
    return create_treemap_sectores(df_sectores)

@app.callback(Output("grafico-empresas", "figure"), [Input("grafico-empresas", "id")])
def update_empresas(_):
    df_empresas = load_csv_data("empresarial.csv")
    return create_funnel_empresas(df_empresas)

@app.callback(Output("grafico-graduados", "figure"), [Input("grafico-graduados", "id")])
def update_graduados(_):
    df_graduados = load_csv_data("graduados_profesion.csv")
    return create_bar_graduados(df_graduados)

@app.callback(Output("grafico-dengue", "figure"), [Input("grafico-dengue", "id")])
def update_dengue(_):
    df_morbilidad = load_csv_data("morbilidad1.csv")
    return create_line_dengue(df_morbilidad)

if __name__ == "__main__":
    logger.info("🚀 Iniciando Dashboard Definitivo...")
    app.run(debug=True, host='127.0.0.1', port=8056)
