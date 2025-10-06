"""
Dashboard de Competitividad de Casanare - Versión Élite
Framework: Dash + Altair + Pydantic
Arquitectura: Multi-página con sidebar fijo
"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import altair as alt
import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Importar módulos de la aplicación
from utils.loader import get_data_loader
# Los imports de los gráficos se harán directamente en los callbacks

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar Altair
alt.data_transformers.enable('json')
alt.themes.enable('default')

# Inicializar aplicación Dash
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    ],
    suppress_callback_exceptions=True
)

app.title = "🏛️ Dashboard de Competitividad de Casanare"

# Cargar datos una sola vez al inicio
logger.info("🚀 Cargando datos...")
data_loader = get_data_loader()
data_loader.load_all_data()
logger.info("✅ Datos cargados exitosamente")

# 🏗️ LAYOUT PRINCIPAL
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    
    # Sidebar fijo
    html.Div([
        html.Div([
            html.H2("🏛️ Casanare", style={'color': 'white', 'marginBottom': '1rem'}),
            html.P("Dashboard de Competitividad", style={'color': '#B0BEC5', 'fontSize': '0.9rem'})
        ], style={'padding': '1rem', 'borderBottom': '1px solid #37474F'}),
        
        html.Nav([
            dbc.Nav([
                dbc.NavLink([
                    html.Span("🏠", style={'marginRight': '0.5rem'}),
                    "Panorama General"
                ], href="/", id="nav-inicio"),
                dbc.NavLink([
                    html.Span("📊", style={'marginRight': '0.5rem'}),
                    "Perfil Económico"
                ], href="/economico", id="nav-economico"),
                dbc.NavLink([
                    html.Span("🏢", style={'marginRight': '0.5rem'}),
                    "Tejido Empresarial"
                ], href="/empresarial", id="nav-empresarial"),
                dbc.NavLink([
                    html.Span("🎓", style={'marginRight': '0.5rem'}),
                    "Educación"
                ], href="/educacion", id="nav-educacion"),
                dbc.NavLink([
                    html.Span("🩺", style={'marginRight': '0.5rem'}),
                    "Salud Pública"
                ], href="/salud", id="nav-salud"),
                dbc.NavLink([
                    html.Span("🛡️", style={'marginRight': '0.5rem'}),
                    "Seguridad Ciudadana"
                ], href="/seguridad", id="nav-seguridad"),
            ], vertical=True, pills=True)
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

# 🏠 PÁGINA DE INICIO
def create_home_page() -> dbc.Container:
    """
    Genera el layout para la página de inicio (Panorama General).

    Esta página muestra los KPIs más importantes y una selección de
    visualizaciones clave de diferentes áreas para ofrecer un resumen
    rápido del estado de competitividad de Casanare.

    Returns:
        dbc.Container: El componente de layout para la página de inicio.
    """
    kpis = data_loader.get_kpis()
    empresas_total = data_loader.get_empresas_total()
    
    return dbc.Container([
        html.H1("🏛️ Dashboard de Competitividad de Casanare", 
               style={'color': '#1f77b4', 'marginBottom': '2rem', 'textAlign': 'center'}),
        
        # KPIs Principales
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("👥 Población", className="text-center"),
                        html.H2(f"{kpis.get('poblacion', 0):,}", className="text-center", 
                                style={'color': '#1f77b4', 'fontSize': '2.5rem'})
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("💰 PIB", className="text-center"),
                        html.H2(f"${kpis.get('pib', 0)/1000000:.1f}B", className="text-center", 
                                style={'color': '#1f77b4', 'fontSize': '2.5rem'})
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🏢 Empresas", className="text-center"),
                        html.H2(f"{empresas_total:,}", className="text-center", 
                                style={'color': '#1f77b4', 'fontSize': '2.5rem'})
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🏆 Ranking", className="text-center"),
                        html.H2(f"#{kpis.get('ranking_idc', 0)}", className="text-center", 
                                style={'color': '#1f77b4', 'fontSize': '2.5rem'})
                    ])
                ])
            ], width=3)
        ], className="mb-4"),
        
        # Visualizaciones principales
        dbc.Row([
            dbc.Col([
                html.H3("📊 Sectores Económicos", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                dcc.Graph(id="grafico-sectores")
            ], width=6),
            dbc.Col([
                html.H3("🏢 Distribución Empresarial", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                dcc.Graph(id="grafico-empresas")
            ], width=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                html.H3("🎓 Graduados por Área", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                dcc.Graph(id="grafico-graduados")
            ], width=6),
            dbc.Col([
                html.H3("🩺 Evolución de Dengue", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                dcc.Graph(id="grafico-dengue")
            ], width=6)
        ])
    ], fluid=True)

# 📊 PÁGINA ECONÓMICA
def create_economic_page() -> dbc.Container:
    """
    Genera el layout para la página de Perfil Económico.

    Esta sección se enfoca en la estructura económica del departamento,
    incluyendo la composición del PIB y la productividad de sectores clave.

    Returns:
        dbc.Container: El componente de layout para la página económica.
    """
    return dbc.Container([
        html.H1("📊 Perfil Económico", style={'color': '#1f77b4', 'marginBottom': '2rem'}),
        
        dbc.Row([
            dbc.Col([
                html.H3("Composición del PIB por Sectores", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                html.Iframe(
                    id="grafico-sectores-economico",
                    style={'width': '100%', 'height': '600px', 'border': 'none'}
                )
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                html.H3("Brechas de Productividad", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                html.Iframe(
                    id="grafico-cultivos",
                    style={'width': '100%', 'height': '600px', 'border': 'none'}
                )
            ], width=12)
        ])
    ], fluid=True)

# 🏢 PÁGINA EMPRESARIAL
def create_empresarial_page() -> dbc.Container:
    """
    Genera el layout para la página de Tejido Empresarial.

    Aquí se analiza la distribución de las empresas por tamaño y su
    concentración geográfica dentro del departamento.

    Returns:
        dbc.Container: El componente de layout para la página empresarial.
    """
    return dbc.Container([
        html.H1("🏢 Tejido Empresarial", style={'color': '#1f77b4', 'marginBottom': '2rem'}),
        
        dbc.Row([
            dbc.Col([
                html.H3("Escala Empresarial", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                html.Iframe(
                    id="grafico-empresas-escala",
                    style={'width': '100%', 'height': '600px', 'border': 'none'}
                )
            ], width=6),
            dbc.Col([
                html.H3("Distribución Geográfica", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                html.Iframe(
                    id="grafico-empresas-geo",
                    style={'width': '100%', 'height': '600px', 'border': 'none'}
                )
            ], width=6)
        ])
    ], fluid=True)

# 🎓 PÁGINA EDUCACIÓN
def create_educacion_page() -> dbc.Container:
    """
    Genera el layout para la página de Educación.

    Esta sección presenta indicadores sobre el capital humano, como el número
    de graduados por área, y la eficiencia del sistema educativo, como la deserción.

    Returns:
        dbc.Container: El componente de layout para la página de educación.
    """
    return dbc.Container([
        html.H1("🎓 Educación", style={'color': '#1f77b4', 'marginBottom': '2rem'}),
        
        dbc.Row([
            dbc.Col([
                html.H3("Capital Humano Formado", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                html.Iframe(
                    id="grafico-graduados-educacion",
                    style={'width': '100%', 'height': '600px', 'border': 'none'}
                )
            ], width=6),
            dbc.Col([
                html.H3("Permanencia en el Sistema", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                html.Iframe(
                    id="grafico-desercion",
                    style={'width': '100%', 'height': '600px', 'border': 'none'}
                )
            ], width=6)
        ])
    ], fluid=True)

# 🩺 PÁGINA SALUD
def create_salud_page() -> dbc.Container:
    """
    Genera el layout para la página de Salud Pública.

    Contiene visualizaciones sobre tendencias de salud importantes,
    como la incidencia de enfermedades de interés público.

    Returns:
        dbc.Container: El componente de layout para la página de salud.
    """
    return dbc.Container([
        html.H1("🩺 Salud Pública", style={'color': '#1f77b4', 'marginBottom': '2rem'}),
        
        dbc.Row([
            dbc.Col([
                html.H3("Tendencias de Salud", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                html.Iframe(
                    id="grafico-salud-tendencias",
                    style={'width': '100%', 'height': '600px', 'border': 'none'}
                )
            ], width=12)
        ])
    ], fluid=True)

# 🛡️ PÁGINA SEGURIDAD
def create_seguridad_page() -> dbc.Container:
    """
    Genera el layout para la página de Seguridad Ciudadana.

    Muestra indicadores clave sobre la incidencia de delitos y la
    seguridad en el departamento.

    Returns:
        dbc.Container: El componente de layout para la página de seguridad.
    """
    return dbc.Container([
        html.H1("🛡️ Seguridad Ciudadana", style={'color': '#1f77b4', 'marginBottom': '2rem'}),
        
        dbc.Row([
            dbc.Col([
                html.H3("Incidencia de Delitos", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                html.Iframe(
                    id="grafico-seguridad",
                    style={'width': '100%', 'height': '600px', 'border': 'none'}
                )
            ], width=12)
        ])
    ], fluid=True)

# 🔄 CALLBACKS
@callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname: str):
    """
    Controlador de navegación principal (Router).

    Este callback se activa cada vez que la URL cambia. Su función es
    renderizar el layout de la página correspondiente al `pathname` de la URL.

    Args:
        pathname (str): La ruta de la URL actual (ej. "/", "/economico").

    Returns:
        Component: El layout de la página a mostrar.
    """
    if pathname == "/":
        return create_home_page()
    elif pathname == "/economico":
        return create_economic_page()
    elif pathname == "/empresarial":
        return create_empresarial_page()
    elif pathname == "/educacion":
        return create_educacion_page()
    elif pathname == "/salud":
        return create_salud_page()
    elif pathname == "/seguridad":
        return create_seguridad_page()
    else:
        return create_home_page()

# --- Callbacks para Gráficos con Plotly ---
@callback(Output("grafico-sectores", "figure"), Input("grafico-sectores", "id"))
def update_sectores_plotly(_):
    """Actualizar gráfico de sectores con Plotly"""
    from pages.graficos_plotly import create_sectores_chart_plotly
    return create_sectores_chart_plotly()

@callback(Output("grafico-empresas", "figure"), Input("grafico-empresas", "id"))
def update_empresas_plotly(_):
    """Actualizar gráfico de empresas con Plotly"""
    from pages.graficos_plotly import create_empresas_chart_plotly
    return create_empresas_chart_plotly()

@callback(Output("grafico-graduados", "figure"), Input("grafico-graduados", "id"))
def update_graduados_plotly(_):
    """Actualizar gráfico de graduados con Plotly"""
    from pages.graficos_plotly import create_graduados_chart_plotly
    return create_graduados_chart_plotly()

@callback(Output("grafico-dengue", "figure"), Input("grafico-dengue", "id"))
def update_dengue_plotly(_):
    """Actualizar gráfico de dengue con Plotly"""
    from pages.graficos_plotly import create_dengue_chart_plotly
    return create_dengue_chart_plotly()


if __name__ == "__main__":
    logger.info("🚀 Iniciando Dashboard de Competitividad de Casanare...")
    # Se desactiva el modo debug para evitar problemas con el auto-reloader en este entorno.
    app.run(debug=False, host='127.0.0.1', port=8057)
