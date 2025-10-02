"""
Dashboard de Competitividad de Casanare - Versión Corregida
Corrección de errores de conexión de datos y KPIs específicos por sector
"""

import dash
from dash import dcc, html, Input, Output, callback, dash_table
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

# 🏗️ FUNCIONES DE CARGA DE DATOS CORREGIDAS
def load_csv_data(filename: str) -> pd.DataFrame:
    """Carga datos CSV con manejo robusto de errores."""
    try:
        file_path = Path("data/clean") / filename
        if not file_path.exists():
            logger.warning(f"Archivo no encontrado: {file_path}")
            return pd.DataFrame()
        
        df = pd.read_csv(file_path)
        
        # Limpiar datos básicos
        df = df.dropna(how='all')
        
        logger.info(f"Datos cargados: {filename} - {len(df)} registros")
        return df
        
    except Exception as e:
        logger.error(f"Error cargando {filename}: {e}")
        return pd.DataFrame()

def get_kpi_values():
    """Extrae KPIs principales desde datos CSV con nombres de columnas correctos."""
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
                kpis['ranking_idc'] = int(valor) if pd.notna(valor) else 0
    except Exception as e:
        logger.error(f"Error procesando datos generales para KPIs: {e}")
        return {}
    
    return kpis

def get_empresas_total():
    """Calcula el total de empresas."""
    df_empresas = load_csv_data("empresarial.csv")
    if df_empresas.empty:
        return 0
    
    try:
        # Usar el nombre correcto de la columna
        df_empresas['número_de_empresas'] = pd.to_numeric(df_empresas['número_de_empresas'], errors='coerce')
        total = df_empresas['número_de_empresas'].sum()
        return int(total) if pd.notna(total) else 0
    except Exception as e:
        logger.error(f"Error calculando total de empresas: {e}")
        return 0

# 🎨 FUNCIONES DE VISUALIZACIÓN CORREGIDAS

def create_treemap_sectores(df_sectores: pd.DataFrame) -> go.Figure:
    """Crea un treemap para mostrar la composición económica con nombres de columnas correctos."""
    if df_sectores.empty:
        return go.Figure().add_annotation(text="No hay datos disponibles", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Limpiar datos con nombres de columnas correctos
    df_clean = df_sectores.copy()
    
    # Usar el nombre correcto de la columna
    if 'participación_porcentual' in df_clean.columns:
        df_clean['participacion_porcentual'] = pd.to_numeric(
            df_clean['participación_porcentual'], errors='coerce'
        )
    else:
        logger.error("Columna 'participación_porcentual' no encontrada")
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
        path=['sector_económico'],
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
    """Crea un gráfico de embudo para mostrar la distribución empresarial."""
    if df_empresas.empty:
        return go.Figure().add_annotation(text="No hay datos disponibles", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Limpiar datos
    df_clean = df_empresas.copy()
    df_clean['número_de_empresas'] = pd.to_numeric(df_clean['número_de_empresas'], errors='coerce')
    
    df_clean = df_clean[df_clean['número_de_empresas'].notna()].copy()
    
    if df_clean.empty:
        return go.Figure().add_annotation(text="No hay datos válidos", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Crear funnel chart
    fig = go.Figure(go.Funnel(
        y=df_clean['tamaño_de_empresa'],
        x=df_clean['número_de_empresas'],
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
    """Crea un gráfico de barras para graduados por área de conocimiento."""
    if df_graduados.empty:
        return go.Figure().add_annotation(text="No hay datos disponibles", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Limpiar datos
    df_clean = df_graduados.copy()
    df_clean['número_de_graduados'] = pd.to_numeric(df_clean['número_de_graduados'], errors='coerce')
    
    df_clean = df_clean[df_clean['número_de_graduados'].notna()].copy()
    df_clean = df_clean.sort_values('número_de_graduados', ascending=True)
    
    if df_clean.empty:
        return go.Figure().add_annotation(text="No hay datos válidos", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Crear gráfico de barras horizontales
    fig = go.Figure()
    
    colors = ['#FF7F0E' if i == 0 else '#1f77b4' for i in range(len(df_clean))]
    
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
        height=400,
        font=dict(family="Inter, Arial, sans-serif", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_line_dengue(df_morbilidad: pd.DataFrame) -> go.Figure:
    """Crea un gráfico de líneas para casos de dengue con manejo correcto de strings."""
    if df_morbilidad.empty:
        return go.Figure().add_annotation(text="No hay datos disponibles", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Filtrar datos de dengue con manejo correcto de strings
    try:
        # Convertir a string si no lo es
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
    
    # Crear gráfico de líneas
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_dengue['año'],
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
        height=400,
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

# Configurar el título de la aplicación
app.title = "🏛️ Dashboard de Competitividad de Casanare"

# 🏛️ LAYOUT PRINCIPAL CON SIDEBAR
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    
    # Sidebar
    html.Div([
        html.Div([
            html.H2("🏛️ Casanare", style={'color': 'white', 'marginBottom': '1rem'}),
            html.P("Dashboard de Competitividad", style={'color': '#B0BEC5', 'fontSize': '0.9rem'})
        ], style={'padding': '1rem', 'borderBottom': '1px solid #37474F'}),
        
        html.Nav([
            dbc.Nav([
                dbc.NavLink([
                    html.Span("🏠", style={'marginRight': '0.5rem'}),
                    "Inicio"
                ], href="/", id="nav-inicio", className="nav-link-custom"),
                dbc.NavLink([
                    html.Span("📊", style={'marginRight': '0.5rem'}),
                    "Perfil Económico"
                ], href="/economico", id="nav-economico", className="nav-link-custom"),
                dbc.NavLink([
                    html.Span("🏢", style={'marginRight': '0.5rem'}),
                    "Tejido Empresarial"
                ], href="/empresarial", id="nav-empresarial", className="nav-link-custom"),
                dbc.NavLink([
                    html.Span("🎓", style={'marginRight': '0.5rem'}),
                    "Educación"
                ], href="/educacion", id="nav-educacion", className="nav-link-custom"),
                dbc.NavLink([
                    html.Span("🩺", style={'marginRight': '0.5rem'}),
                    "Salud Pública"
                ], href="/salud", id="nav-salud", className="nav-link-custom"),
                dbc.NavLink([
                    html.Span("🛡️", style={'marginRight': '0.5rem'}),
                    "Seguridad Ciudadana"
                ], href="/seguridad", id="nav-seguridad", className="nav-link-custom"),
            ], vertical=True, pills=True, className="flex-column")
        ], style={'padding': '1rem'})
    ], style={
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'width': '250px',
        'height': '100vh',
        'background': 'linear-gradient(180deg, #1f77b4 0%, #0d47a1 100%)',
        'zIndex': 1000,
        'boxShadow': '2px 0 10px rgba(0,0,0,0.1)'
    }),
    
    # Contenido principal
    html.Div(id="page-content", style={'marginLeft': '250px', 'padding': '2rem'})
])

# 🏠 PÁGINA DE INICIO - RESUMEN EJECUTIVO
def create_home_page():
    return dbc.Container([
        # Header
        html.Div([
            html.H1("🏛️ Dashboard de Competitividad de Casanare", 
                   style={'color': '#1f77b4', 'marginBottom': '0.5rem'}),
            html.P("Análisis Integral y Recomendaciones Estratégicas", 
                  style={'color': '#666', 'fontSize': '1.1rem'})
        ], style={'marginBottom': '2rem'}),
        
        # KPIs Principales - CORREGIDOS
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Span("👥", style={"fontSize": "3rem", "display": "block", "textAlign": "center"}),
                            html.H4("Población", className="card-title text-center"),
                            html.H2(id="kpi-poblacion", className="text-center", style={'color': '#1f77b4', 'fontSize': '2.5rem', 'fontWeight': '700'}),
                            html.P("Proyección 2025", className="text-muted text-center")
                        ])
                    ])
                ], style={'height': '200px', 'display': 'flex', 'alignItems': 'center'})
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Span("💰", style={"fontSize": "3rem", "display": "block", "textAlign": "center"}),
                            html.H4("PIB Departamental", className="card-title text-center"),
                            html.H2(id="kpi-pib", className="text-center", style={'color': '#1f77b4', 'fontSize': '2.5rem', 'fontWeight': '700'}),
                            html.P("2023", className="text-muted text-center")
                        ])
                    ])
                ], style={'height': '200px', 'display': 'flex', 'alignItems': 'center'})
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Span("🏢", style={"fontSize": "3rem", "display": "block", "textAlign": "center"}),
                            html.H4("Empresas Totales", className="card-title text-center"),
                            html.H2(id="kpi-empresas", className="text-center", style={'color': '#1f77b4', 'fontSize': '2.5rem', 'fontWeight': '700'}),
                            html.P("Registradas", className="text-muted text-center")
                        ])
                    ])
                ], style={'height': '200px', 'display': 'flex', 'alignItems': 'center'})
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Span("🏆", style={"fontSize": "3rem", "display": "block", "textAlign": "center"}),
                            html.H4("Ranking IDC", className="card-title text-center"),
                            html.H2(id="kpi-ranking", className="text-center", style={'color': '#1f77b4', 'fontSize': '2.5rem', 'fontWeight': '700'}),
                            html.P("Nacional", className="text-muted text-center")
                        ])
                    ])
                ], style={'height': '200px', 'display': 'flex', 'alignItems': 'center'})
            ], width=3)
        ], className="mb-4"),
        
        # Visualizaciones "Gancho"
        html.H3("📊 Panorama General", style={'color': '#1f77b4', 'marginBottom': '2rem'}),
        dbc.Row([
            dbc.Col([
                html.H5("🏭 Composición Económica", style={'color': '#1f77b4'}),
                dcc.Graph(id="grafico-treemap-inicio")
            ], width=6),
            dbc.Col([
                html.H5("🏢 Estructura Empresarial", style={'color': '#1f77b4'}),
                dcc.Graph(id="grafico-funnel-inicio")
            ], width=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                html.H5("🎓 Panorama Educativo", style={'color': '#1f77b4'}),
                dcc.Graph(id="grafico-educacion-inicio")
            ], width=6),
            dbc.Col([
                html.H5("🩺 Tendencia de Salud Crítica", style={'color': '#1f77b4'}),
                dcc.Graph(id="grafico-salud-inicio")
            ], width=6)
        ])
    ], fluid=True)

# 📊 PÁGINA DE PERFIL ECONÓMICO
def create_economic_page():
    return dbc.Container([
        html.H1("📊 Perfil Económico de Casanare", 
               style={'color': '#1f77b4', 'marginBottom': '2rem'}),
        
        # Visualización Principal
        dbc.Row([
            dbc.Col([
                html.H3("🏭 Composición del PIB por Sectores", style={'color': '#1f77b4'}),
                dcc.Graph(id="grafico-treemap-economico")
            ], width=12)
        ], className="mb-4"),
        
        # Insights y Recomendaciones
        dbc.Row([
            dbc.Col([
                html.H3("💡 Insights Clave y Recomendaciones Estratégicas", 
                       style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                dbc.Alert([
                    html.H5("🎯 Insights Clave:"),
                    html.P("• La economía de Casanare muestra una dependencia crítica del sector de minas y canteras, que representa más del 50% del PIB departamental, creando una alta vulnerabilidad a la volatilidad de los precios de los commodities."),
                    html.P("• La concentración económica en un solo sector limita la diversificación y el desarrollo de otros sectores productivos con potencial de crecimiento."),
                    html.Hr(),
                    html.H5("🚀 Recomendaciones Estratégicas:"),
                    html.P("• Implementar un fondo de diversificación económica financiado con un porcentaje de las regalías para co-invertir en proyectos de agroindustria (palma y arroz) y turismo sostenible, con el objetivo de reducir la dependencia del sector extractivo en un 15% en los próximos 5 años."),
                    html.P("• Desarrollar un programa de incubación de empresas en sectores de servicios y tecnología, aprovechando la infraestructura existente y el capital humano disponible.")
                ], color="info")
            ], width=12)
        ])
    ], fluid=True)

# 🔄 CALLBACKS PARA NAVEGACIÓN
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    """Actualiza el contenido según la URL."""
    if pathname == "/":
        return create_home_page()
    elif pathname == "/economico":
        return create_economic_page()
    else:
        return create_home_page()

# 🔄 CALLBACKS PARA ACTUALIZAR DATOS - CORREGIDOS
@app.callback(
    [Output("kpi-poblacion", "children"),
     Output("kpi-pib", "children"),
     Output("kpi-empresas", "children"),
     Output("kpi-ranking", "children")],
    [Input("kpi-poblacion", "id")]
)
def update_kpis(_):
    """Actualiza los KPIs principales con datos correctos."""
    try:
        kpis = get_kpi_values()
        
        poblacion = kpis.get('poblacion_2025', 0)
        pib = kpis.get('pib_2023', 0)
        ranking = kpis.get('ranking_idc', 0)
        
        # Calcular empresas totales
        empresas_totales = get_empresas_total()
        
        # Formatear valores
        poblacion_str = f"{poblacion:,}" if poblacion > 0 else "N/A"
        pib_billones = pib / 1000000 if pib > 0 else 0
        pib_str = f"${pib_billones:.1f}B" if pib_billones > 0 else "N/A"
        empresas_str = f"{empresas_totales:,}" if empresas_totales > 0 else "N/A"
        ranking_str = f"#{ranking}" if ranking > 0 else "N/A"
        
        logger.info(f"KPIs actualizados - Población: {poblacion_str}, PIB: {pib_str}, Empresas: {empresas_str}, Ranking: {ranking_str}")
        
        return poblacion_str, pib_str, empresas_str, ranking_str
        
    except Exception as e:
        logger.error(f"Error actualizando KPIs: {e}")
        return "Error", "Error", "Error", "Error"

# Callbacks para visualizaciones de inicio - CORREGIDOS
@app.callback(
    Output("grafico-treemap-inicio", "figure"),
    [Input("grafico-treemap-inicio", "id")]
)
def update_treemap_inicio(_):
    """Actualiza el treemap de inicio con nombres de columnas correctos."""
    try:
        df_sectores = load_csv_data("sector_economico.csv")
        return create_treemap_sectores(df_sectores)
    except Exception as e:
        logger.error(f"Error actualizando treemap inicio: {e}")
        return go.Figure().add_annotation(text=f"Error: {e}", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)

@app.callback(
    Output("grafico-funnel-inicio", "figure"),
    [Input("grafico-funnel-inicio", "id")]
)
def update_funnel_inicio(_):
    """Actualiza el funnel de inicio."""
    try:
        df_empresas = load_csv_data("empresarial.csv")
        return create_funnel_empresas(df_empresas)
    except Exception as e:
        logger.error(f"Error actualizando funnel inicio: {e}")
        return go.Figure().add_annotation(text=f"Error: {e}", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)

@app.callback(
    Output("grafico-educacion-inicio", "figure"),
    [Input("grafico-educacion-inicio", "id")]
)
def update_educacion_inicio(_):
    """Actualiza el gráfico de educación de inicio."""
    try:
        df_graduados = load_csv_data("graduados_profesion.csv")
        return create_bar_graduados(df_graduados)
    except Exception as e:
        logger.error(f"Error actualizando educación inicio: {e}")
        return go.Figure().add_annotation(text=f"Error: {e}", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)

@app.callback(
    Output("grafico-salud-inicio", "figure"),
    [Input("grafico-salud-inicio", "id")]
)
def update_salud_inicio(_):
    """Actualiza el gráfico de salud de inicio con manejo correcto de strings."""
    try:
        df_morbilidad = load_csv_data("morbilidad1.csv")
        return create_line_dengue(df_morbilidad)
    except Exception as e:
        logger.error(f"Error actualizando salud inicio: {e}")
        return go.Figure().add_annotation(text=f"Error: {e}", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)

# Callback para página económica
@app.callback(
    Output("grafico-treemap-economico", "figure"),
    [Input("grafico-treemap-economico", "id")]
)
def update_treemap_economico(_):
    """Actualiza el treemap de la página económica."""
    try:
        df_sectores = load_csv_data("sector_economico.csv")
        return create_treemap_sectores(df_sectores)
    except Exception as e:
        logger.error(f"Error actualizando treemap económico: {e}")
        return go.Figure().add_annotation(text=f"Error: {e}", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)

# 🚀 EJECUTAR LA APLICACIÓN
if __name__ == "__main__":
    logger.info("🚀 Iniciando Dashboard Corregido...")
    app.run(debug=True, host='127.0.0.1', port=8054)
