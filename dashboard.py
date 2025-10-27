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
    generalidades_df = data_loader.get_data('generalidades')

    def extract_indicator(keyword: str):
        if generalidades_df.empty:
            return None
        df_match = generalidades_df[generalidades_df['indicador'].str.contains(keyword, case=False, na=False)]
        if df_match.empty:
            return None
        row = df_match.sort_values('ao', ascending=False).iloc[0]
        raw_value = pd.to_numeric(str(row['valor']).replace(',', '.'), errors='coerce')
        if pd.isna(raw_value):
            return None
        year = int(row['ao']) if 'ao' in row and pd.notna(row['ao']) else None
        unit = row['unidad'] if 'unidad' in row and pd.notna(row['unidad']) else None
        return {'value': float(raw_value), 'year': year, 'unit': unit}

    def format_currency(value: float) -> str:
        return f"${value:,.0f}"

    def format_number(value: float) -> str:
        return f"{value:,.0f}"

    indicator_specs = [
        {
            'query': 'PIB per cápita',
            'label': 'PIB per cápita',
            'description': 'Ingreso promedio por habitante',
            'formatter': lambda data: f"{format_currency(data['value'])} COP"
        },
        {
            'query': 'Cobertura neta en educación media',
            'label': 'Cobertura neta en educación media',
            'description': 'Calidad y cobertura educativa',
            'formatter': lambda data: f"{data['value']:.2f} / 10"
        },
        {
            'query': 'Costo de la energía eléctrica',
            'label': 'Costo de la energía eléctrica',
            'description': 'Competitividad del entorno productivo',
            'formatter': lambda data: f"{data['value']:.1f} / 10"
        },
        {
            'query': 'Frontera Agrícola',
            'label': 'Frontera agrícola',
            'description': 'Superficie disponible para producción',
            'formatter': lambda data: f"{format_number(data['value'])} hectáreas"
        },
        {
            'query': 'Inventario Ganadero Bovino',
            'label': 'Inventario ganadero',
            'description': 'Capacidad productiva pecuaria',
            'formatter': lambda data: f"{format_number(data['value'])} cabezas"
        }
    ]

    indicator_items = []
    indicator_map = {}
    for spec in indicator_specs:
        data = extract_indicator(spec['query'])
        if not data:
            continue
        indicator_map[spec['label']] = data
        value_text = spec['formatter'](data)
        indicator_items.append(
            dbc.ListGroupItem([
                html.Div([
                    html.Span(spec['label'], className="fw-semibold"),
                    html.Span(str(data['year']) if data['year'] else '', className="text-muted")
                ], className="d-flex justify-content-between align-items-center"),
                html.Div(value_text, className="fs-5 fw-bold text-primary"),
                html.Small(spec['description'], className="text-muted")
            ], className="py-3")
        )

    insights_lines = []
    if indicator_map.get('PIB per cápita'):
        data = indicator_map['PIB per cápita']
        insights_lines.append(f"**PIB per cápita:** {format_currency(data['value'])} COP (dato {data['year']}).")
    if indicator_map.get('Inventario ganadero'):
        data = indicator_map['Inventario ganadero']
        insights_lines.append(f"**Inventario ganadero:** {format_number(data['value'])} cabezas estimadas en {data['year']}.")
    if indicator_map.get('Frontera agrícola'):
        data = indicator_map['Frontera agrícola']
        insights_lines.append(f"**Frontera agrícola:** {format_number(data['value'])} hectáreas disponibles ({data['year']}).")
    if indicator_map.get('Cobertura neta en educación media'):
        data = indicator_map['Cobertura neta en educación media']
        insights_lines.append(f"**Cobertura neta en educación media:** {data['value']:.2f}/10 según IDC {data['year']}.")
    if indicator_map.get('Costo de la energía eléctrica'):
        data = indicator_map['Costo de la energía eléctrica']
        insights_lines.append(f"**Costo de la energía:** evaluación de {data['value']:.1f}/10 ({data['year']}).")
    if kpis.get('ranking_idc'):
        insights_lines.append(f"**Posición en el IDC:** Casanare ocupa el puesto #{kpis['ranking_idc']} a nivel nacional.")

    insights_md = "\n".join(f"- {line}" for line in insights_lines) if insights_lines else ""

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

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Indicadores estratégicos"),
                    dbc.CardBody([
                        html.P(
                            "Últimos datos publicados por el Índice Departamental de Competitividad.",
                            className="text-muted small"
                        ),
                        dbc.ListGroup(indicator_items, flush=True) if indicator_items else html.P(
                            "Aún no hay indicadores destacados para mostrar.", className="text-muted"
                        )
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Lo que revela el territorio"),
                    dbc.CardBody([
                        dcc.Markdown(insights_md, className="mb-0") if insights_md else html.P(
                            "Cuando se actualicen los indicadores se mostrará aquí un resumen interpretativo.",
                            className="text-muted"
                        )
                    ])
                ])
            ], width=6)
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
                    srcDoc="",
                    style={'width': '100%', 'height': '600px', 'border': 'none'}
                )
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                html.H3("Brechas de Productividad", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                html.Iframe(
                    id="grafico-cultivos",
                    srcDoc="",
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
                    srcDoc="",
                    style={'width': '100%', 'height': '600px', 'border': 'none'}
                )
            ], width=6),
            dbc.Col([
                html.H3("Distribución Geográfica", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                html.Iframe(
                    id="grafico-empresas-geo",
                    srcDoc="",
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
                    srcDoc="",
                    style={'width': '100%', 'height': '600px', 'border': 'none'}
                )
            ], width=6),
            dbc.Col([
                html.H3("Permanencia en el Sistema", style={'color': '#1f77b4', 'marginBottom': '1rem'}),
                html.Iframe(
                    id="grafico-desercion",
                    srcDoc="",
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
                    srcDoc="",
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
                    srcDoc="",
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


@callback(Output("grafico-sectores-economico", "srcDoc"), Input("grafico-sectores-economico", "id"))
def render_sectores_economico(_):
    """Renderiza la composición sectorial del PIB."""
    from utils.plotting import create_sectores_economico_chart

    return create_sectores_economico_chart()


@callback(Output("grafico-cultivos", "srcDoc"), Input("grafico-cultivos", "id"))
def render_cultivos(_):
    """Renderiza las brechas de productividad agropecuaria."""
    from utils.plotting import create_cultivos_chart

    return create_cultivos_chart()


@callback(Output("grafico-empresas-escala", "srcDoc"), Input("grafico-empresas-escala", "id"))
def render_empresas_escala(_):
    """Renderiza el gráfico de escala empresarial."""
    from utils.plotting import create_empresas_escala_chart

    return create_empresas_escala_chart()


@callback(Output("grafico-empresas-geo", "srcDoc"), Input("grafico-empresas-geo", "id"))
def render_empresas_geo(_):
    """Renderiza la distribución geográfica de empresas."""
    from utils.plotting import create_empresas_geo_chart

    return create_empresas_geo_chart()


@callback(Output("grafico-graduados-educacion", "srcDoc"), Input("grafico-graduados-educacion", "id"))
def render_graduados_educacion(_):
    """Renderiza el gráfico de graduados en la página de Educación."""
    from utils.plotting import create_graduados_educacion_chart

    return create_graduados_educacion_chart()


@callback(Output("grafico-desercion", "srcDoc"), Input("grafico-desercion", "id"))
def render_desercion(_):
    """Renderiza la evolución de la deserción escolar."""
    from utils.plotting import create_desercion_chart

    return create_desercion_chart()


@callback(Output("grafico-salud-tendencias", "srcDoc"), Input("grafico-salud-tendencias", "id"))
def render_salud_tendencias(_):
    """Renderiza las tendencias de salud pública."""
    from utils.plotting import create_salud_tendencias_chart

    return create_salud_tendencias_chart()


@callback(Output("grafico-seguridad", "srcDoc"), Input("grafico-seguridad", "id"))
def render_seguridad(_):
    """Renderiza los indicadores de seguridad ciudadana."""
    from utils.plotting import create_seguridad_chart

    return create_seguridad_chart()


if __name__ == "__main__":
    logger.info("🚀 Iniciando Dashboard de Competitividad de Casanare...")
    # Se desactiva el modo debug para evitar problemas con el auto-reloader en este entorno.
    app.run(debug=False, host='127.0.0.1', port=8057)
