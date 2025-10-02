"""
Dashboard de Competitividad de Casanare - VERSIÓN ÉLITE
Combinación de Plotly (robusto) + Altair (académico) + Multi-página
"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Importar cargador de datos
from utils.loader_v3 import get_data_loader

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar Altair
alt.data_transformers.enable('json')

# Inicializar aplicación Dash
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    ],
    suppress_callback_exceptions=True
)

app.title = "🏛️ Dashboard de Competitividad de Casanare - Élite"

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
def create_home_page():
    """Crear página de inicio con KPIs principales"""
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
def create_economic_page():
    """Crear página de perfil económico"""
    return dbc.Container([
        html.H1("📊 Perfil Económico", style={'color': '#1f77b4', 'marginBottom': '2rem'}),
        
        # Narrativa
        dbc.Alert([
            html.H4("🎯 Narrativa Económica", className="alert-heading"),
            html.P("Casanare es una potencia energética con un sector agrícola prometedor pero con brechas de productividad significativas. El análisis revela la dominancia del sector minero-energético y las oportunidades de diversificación económica."),
        ], color="info", className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                html.H3("Composición del PIB por Sectores", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                dcc.Graph(id="grafico-sectores-economico")
            ], width=12)
        ], className="mb-4"),
        
        # Insights y Recomendaciones
        dbc.Row([
            dbc.Col([
                html.H4("💡 Insights Clave", style={'color': '#1f77b4'}),
                html.Ul([
                    html.Li("El sector minero-energético representa más del 50% del PIB departamental"),
                    html.Li("Existe una alta concentración en pocos sectores económicos"),
                    html.Li("Las brechas de productividad agrícola representan oportunidades de mejora")
                ])
            ], width=6),
            dbc.Col([
                html.H4("🚀 Recomendaciones Estratégicas", style={'color': '#1f77b4'}),
                html.Ul([
                    html.Li("Diversificar la base económica para reducir dependencia del petróleo"),
                    html.Li("Invertir en tecnología agrícola para cerrar brechas de productividad"),
                    html.Li("Desarrollar clusters industriales alrededor de los recursos naturales")
                ])
            ], width=6)
        ])
    ], fluid=True)

# 🏢 PÁGINA EMPRESARIAL
def create_empresarial_page():
    """Crear página de tejido empresarial"""
    return dbc.Container([
        html.H1("🏢 Tejido Empresarial", style={'color': '#1f77b4', 'marginBottom': '2rem'}),
        
        # Narrativa
        dbc.Alert([
            html.H4("🎯 Narrativa Empresarial", className="alert-heading"),
            html.P("El motor empresarial de Casanare es vasto pero atomizado en microempresas, con una fuerte concentración geográfica en la capital. Esta estructura presenta tanto desafíos como oportunidades para el desarrollo económico."),
        ], color="info", className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                html.H3("Escala Empresarial", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                dcc.Graph(id="grafico-empresas-escala")
            ], width=6),
            dbc.Col([
                html.H3("Distribución Geográfica", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                dcc.Graph(id="grafico-empresas-geo")
            ], width=6)
        ])
    ], fluid=True)

# 🎓 PÁGINA EDUCACIÓN
def create_educacion_page():
    """Crear página de educación"""
    return dbc.Container([
        html.H1("🎓 Educación", style={'color': '#1f77b4', 'marginBottom': '2rem'}),
        
        # Narrativa
        dbc.Alert([
            html.H4("🎯 Narrativa Educativa", className="alert-heading"),
            html.P("Existe un desajuste entre el capital humano que se está formando y los principales motores económicos del departamento. El análisis revela oportunidades para alinear la formación con las necesidades del mercado laboral."),
        ], color="info", className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                html.H3("Capital Humano Formado", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                dcc.Graph(id="grafico-graduados-educacion")
            ], width=6),
            dbc.Col([
                html.H3("Permanencia en el Sistema", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                dcc.Graph(id="grafico-desercion")
            ], width=6)
        ])
    ], fluid=True)

# 🩺 PÁGINA SALUD
def create_salud_page():
    """Crear página de salud pública"""
    return dbc.Container([
        html.H1("🩺 Salud Pública", style={'color': '#1f77b4', 'marginBottom': '2rem'}),
        
        # Narrativa
        dbc.Alert([
            html.H4("🎯 Narrativa de Salud", className="alert-heading"),
            html.P("Aunque se observan mejoras en algunos indicadores, persisten desafíos críticos en enfermedades transmisibles y salud reproductiva. El monitoreo continuo es esencial para la salud pública departamental."),
        ], color="info", className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                html.H3("Tendencias de Salud", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                dcc.Graph(id="grafico-salud-tendencias")
            ], width=12)
        ])
    ], fluid=True)

# 🛡️ PÁGINA SEGURIDAD
def create_seguridad_page():
    """Crear página de seguridad ciudadana"""
    return dbc.Container([
        html.H1("🛡️ Seguridad Ciudadana", style={'color': '#1f77b4', 'marginBottom': '2rem'}),
        
        # Narrativa
        dbc.Alert([
            html.H4("🎯 Narrativa de Seguridad", className="alert-heading"),
            html.P("El análisis de la seguridad se centra en delitos de alto impacto, donde el hurto a personas representa el desafío más significativo en términos de volumen. La estrategia debe priorizar la prevención y el fortalecimiento institucional."),
        ], color="info", className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                html.H3("Incidencia de Delitos", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                dcc.Graph(id="grafico-seguridad")
            ], width=12)
        ])
    ], fluid=True)

# 🔄 CALLBACKS
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    """Mostrar página según la URL"""
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

# Callbacks para gráficos
@app.callback(Output("grafico-sectores", "figure"), [Input("grafico-sectores", "id")])
def update_sectores(_):
    """Actualizar gráfico de sectores con Plotly"""
    df = data_loader.get_sectores_economicos()
    
    if df.empty:
        return go.Figure().add_annotation(text="No hay datos disponibles", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Crear treemap
    fig = px.treemap(
        df,
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

@app.callback(Output("grafico-empresas", "figure"), [Input("grafico-empresas", "id")])
def update_empresas(_):
    """Actualizar gráfico de empresas con Plotly"""
    df = data_loader.get_empresas_por_tamano()
    
    if df.empty:
        return go.Figure().add_annotation(text="No hay datos disponibles", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Crear funnel chart
    fig = go.Figure(go.Funnel(
        y=df['tamano_de_empresa'],
        x=df['numero_de_empresas'],
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

@app.callback(Output("grafico-graduados", "figure"), [Input("grafico-graduados", "id")])
def update_graduados(_):
    """Actualizar gráfico de graduados con Plotly"""
    df = data_loader.get_graduados_por_area()
    
    if df.empty:
        return go.Figure().add_annotation(text="No hay datos disponibles", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Ordenar por número de graduados
    df = df.sort_values('numero_de_graduados', ascending=True)
    
    # Crear gráfico de barras horizontales
    fig = go.Figure()
    
    colors = ['#FF7F0E' if i == len(df)-1 else '#1f77b4' for i in range(len(df))]
    
    fig.add_trace(go.Bar(
        y=df['area_de_conocimiento'],
        x=df['numero_de_graduados'],
        orientation='h',
        marker=dict(color=colors),
        text=[f"{val:,.0f}" for val in df['numero_de_graduados']],
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

@app.callback(Output("grafico-dengue", "figure"), [Input("grafico-dengue", "id")])
def update_dengue(_):
    """Actualizar gráfico de dengue con Plotly"""
    df = data_loader.get_dengue_data()
    
    if df.empty:
        return go.Figure().add_annotation(text="No hay datos disponibles", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Crear gráfico de líneas
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['a_o'],
        y=df['valor'],
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

# Callbacks para páginas específicas
@app.callback(Output("grafico-sectores-economico", "figure"), [Input("grafico-sectores-economico", "id")])
def update_sectores_economico(_):
    """Actualizar gráfico de sectores para página económica"""
    return update_sectores(_)

@app.callback(Output("grafico-empresas-escala", "figure"), [Input("grafico-empresas-escala", "id")])
def update_empresas_escala(_):
    """Actualizar gráfico de empresas para página empresarial"""
    return update_empresas(_)

@app.callback(Output("grafico-graduados-educacion", "figure"), [Input("grafico-graduados-educacion", "id")])
def update_graduados_educacion(_):
    """Actualizar gráfico de graduados para página educación"""
    return update_graduados(_)

@app.callback(Output("grafico-desercion", "figure"), [Input("grafico-desercion", "id")])
def update_desercion(_):
    """Actualizar gráfico de deserción"""
    df = data_loader.get_desercion_data()
    
    if df.empty:
        return go.Figure().add_annotation(text="No hay datos disponibles", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Crear gráfico de líneas por municipio
    fig = go.Figure()
    
    for municipio in df['municipio'].unique():
        df_municipio = df[df['municipio'] == municipio]
        fig.add_trace(go.Scatter(
            x=df_municipio['año'],
            y=df_municipio['tasa_desercion'],
            mode='lines+markers',
            name=municipio,
            hovertemplate=f"<b>{municipio}</b><br>" +
                         "Año: %{x}<br>" +
                         "Tasa: %{y:.2%}<br>" +
                         "<extra></extra>"
        ))
    
    fig.update_layout(
        title="<b>Evolución de Tasa de Deserción por Municipio</b>",
        xaxis_title="Año",
        yaxis_title="Tasa de Deserción",
        height=500,
        font=dict(family="Inter, Arial, sans-serif", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

@app.callback(Output("grafico-salud-tendencias", "figure"), [Input("grafico-salud-tendencias", "id")])
def update_salud_tendencias(_):
    """Actualizar gráfico de tendencias de salud"""
    return update_dengue(_)

@app.callback(Output("grafico-seguridad", "figure"), [Input("grafico-seguridad", "id")])
def update_seguridad(_):
    """Actualizar gráfico de seguridad"""
    df = data_loader.get_seguridad_data()
    
    if df.empty:
        return go.Figure().add_annotation(text="No hay datos disponibles", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # Crear gráfico de barras horizontales
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df['indicador'],
        x=df['valor'],
        orientation='h',
        marker=dict(color='#d62728'),
        text=[f"{val:,.0f}" for val in df['valor']],
        textposition='outside',
        textfont=dict(size=11, color='#333333'),
        hovertemplate="<b>%{y}</b><br>" +
                     "Casos: %{x:,.0f}<br>" +
                     "<extra></extra>",
        showlegend=False
    ))
    
    fig.update_layout(
        title="<b>Incidencia de Delitos en Casanare</b>",
        xaxis_title="Número de Casos",
        yaxis_title="",
        height=500,
        font=dict(family="Inter, Arial, sans-serif", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

if __name__ == "__main__":
    logger.info("🚀 Iniciando Dashboard Élite de Competitividad de Casanare...")
    app.run(debug=True, host='127.0.0.1', port=8058)
