"""
Módulo modernizado para la creación de visualizaciones con Plotly.
Funciones específicas para cada tipo de gráfico del dashboard.
Optimizado para legibilidad en modo claro y oscuro.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# 🎨 PALETA DE COLORES CORPORATIVA CASANARE
COLORS = {
    'primary': '#1f77b4',        # Azul corporativo
    'secondary': '#ff7f0e',      # Naranja
    'success': '#2ca02c',        # Verde
    'warning': '#d62728',        # Rojo
    'info': '#9467bd',           # Púrpura
    'casanare_blue': '#0066CC',  # Azul Casanare
    'casanare_yellow': '#FFD700', # Amarillo Casanare
    'casanare_green': '#228B22',  # Verde Casanare
    'text_dark': '#333333',      # Texto oscuro para legibilidad
    'corporate': ['#0066CC', '#FFD700', '#228B22', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
}

# 🎨 CONFIGURACIÓN UNIVERSAL PARA GRÁFICOS
def apply_universal_layout(fig, title=""):
    """
    Aplica configuración universal para legibilidad en modo claro y oscuro.
    """
    fig.update_layout(
        # Fondos transparentes para adaptarse al tema de Streamlit - MEJORADO
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        
        # Texto oscuro para máxima legibilidad en cualquier modo
        font=dict(
            family="Inter, Arial, sans-serif",
            size=12,
            color='#333333'  # Color fijo para legibilidad universal
        ),
        
        # Título centrado y visible
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            font=dict(size=16, color=COLORS['text_dark'], family="Inter")
        ),
        
        # Ejes con colores definidos - CORREGIDO ValueError
        xaxis=dict(
            gridcolor='rgba(128,128,128,0.2)',
            tickfont=dict(color=COLORS['text_dark']),
            title=dict(
                font=dict(color=COLORS['text_dark'], size=14)
            )
        ),
        yaxis=dict(
            gridcolor='rgba(128,128,128,0.2)',
            tickfont=dict(color=COLORS['text_dark']),
            title=dict(
                font=dict(color=COLORS['text_dark'], size=14)
            )
        ),
        
        # Leyenda legible
        legend=dict(
            font=dict(color=COLORS['text_dark'])
        )
    )
    return fig

def plot_treemap_sectores(df_sectores):
    """
    Crea un treemap moderno para mostrar la participación de sectores económicos.
    OPTIMIZADO para legibilidad en modo claro y oscuro.
    
    Args:
        df_sectores (pd.DataFrame): DataFrame con datos de sectores económicos
        
    Returns:
        plotly.graph_objects.Figure: Figura de treemap configurada
    """
    if df_sectores.empty:
        return go.Figure()
    
    fig = px.treemap(
        df_sectores,
        path=['sector_economico'],
        values='participacion_porcentual',
        title='🏭 Participación de Sectores Económicos en el PIB',
        color='participacion_porcentual',
        color_continuous_scale='YlGnBu',
        hover_data={'participacion_porcentual': ':.1f'}
    )
    
    fig.update_traces(
        textinfo="label+percent entry",
        textfont_size=14,  # TAMAÑO AUMENTADO para mejor legibilidad
        textfont_color='black',  # NEGRO FIJO para máxima legibilidad sobre cualquier color
        textfont_family="Inter",
        hovertemplate="<b>%{label}</b><br>" +
                     "Participación: %{value:.1f}%<br>" +
                     "<extra></extra>",
        # Bordes para mejor definición
        marker=dict(line=dict(color='white', width=2))
    )
    
    # Aplicar configuración universal
    fig = apply_universal_layout(fig, "🏭 Participación de Sectores Económicos en el PIB")
    
    fig.update_layout(
        height=600,
        coloraxis_showscale=False
    )
    
    return fig

def plot_treemap_sectores_mejorado(df_sectores):
    """
    Crea un treemap mejorado para mostrar la participación de sectores económicos.
    CORREGIDO para usar nombres de columnas reales y colores más vivos.
    OPTIMIZADO para legibilidad universal.
    
    Args:
        df_sectores (pd.DataFrame): DataFrame con datos de sectores económicos
        
    Returns:
        plotly.graph_objects.Figure: Figura de treemap configurada
    """
    if df_sectores.empty:
        return go.Figure()
    
    # Filtrar datos válidos y excluir el total
    df_limpio = df_sectores[
        (df_sectores['sector_economico'] != 'Total') & 
        (df_sectores['participacion_porcentual_porcentaje'].notna()) &
        (df_sectores['participacion_porcentual_porcentaje'] > 0)
    ].copy()
    
    if df_limpio.empty:
        # Si no hay datos válidos, mostrar mensaje
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos válidos para mostrar",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        return fig
    
    # Crear treemap con colores más vivos
    fig = px.treemap(
        df_limpio,
        path=['sector_economico'],  # Nombre correcto de la columna
        values='participacion_porcentual_porcentaje',  # Nombre correcto de la columna
        title='<b>🏭 Participación de Sectores Económicos en el PIB</b>',
        color='participacion_porcentual_porcentaje',
        # Colores más vivos y contrastantes
        color_continuous_scale='Viridis',  # Escala más vibrante
        hover_data={'participacion_porcentual_porcentaje': ':.1f'}
    )
    
    fig.update_traces(
        textinfo="label+percent entry",
        textfont_size=14,  # Tamaño grande para legibilidad
        textfont_color='white',  # Texto blanco para contraste
        textfont_family="Inter",
        hovertemplate="<b>%{label}</b><br>" +
                     "Participación: %{value:.1f}%<br>" +
                     "<extra></extra>",
        # Bordes blancos para mejor definición
        marker=dict(line=dict(color='white', width=2))
    )
    
    # Aplicar configuración universal
    fig = apply_universal_layout(fig, "🏭 Participación de Sectores Económicos en el PIB")
    
    fig.update_layout(
        height=600,
        coloraxis_showscale=False,
        margin=dict(t=50, l=25, r=25, b=25)
    )
    
    return fig

def plot_funnel_empresas(df_empresarial):
    """
    Crea un gráfico de embudo para mostrar la distribución de empresas por tamaño.
    Más narrativo que un gráfico de barras para mostrar el "filtrado" empresarial.
    OPTIMIZADO para legibilidad universal.
    
    Args:
        df_empresarial (pd.DataFrame): DataFrame con datos de empresas por tamaño
        
    Returns:
        plotly.graph_objects.Figure: Figura de embudo configurada
    """
    if df_empresarial.empty:
        return go.Figure()
    
    # Ordenar por número de empresas (de mayor a menor para el embudo)
    df_sorted = df_empresarial.sort_values('numero_de_empresas', ascending=False)
    
    fig = px.funnel(
        df_sorted,
        x='numero_de_empresas',
        y='tamaño_de_empresa',
        title='<b>🏢 Distribución de Empresas por Tamaño (Embudo)</b>',
        color='numero_de_empresas',
        color_continuous_scale='Blues',
        hover_data={'numero_de_empresas': ':,f'}
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='value+label',
        textfont_size=12,
        textfont_color='white',
        textfont_family="Inter",
        hovertemplate="<b>%{y}</b><br>" +
                     "Empresas: %{x:,}<br>" +
                     "<extra></extra>"
    )
    
    # Aplicar configuración universal
    fig = apply_universal_layout(fig, "🏢 Distribución de Empresas por Tamaño (Embudo)")
    
    fig.update_layout(
        height=500,
        coloraxis_showscale=False,
        xaxis_title="Número de Empresas",
        yaxis_title="Tamaño de Empresa"
    )
    
    return fig

def plot_area_evolucion(df, x_col, y_col, title, y_title=""):
    """
    Crea un gráfico de área para mostrar evolución temporal.
    Más impactante que una línea simple para mostrar tendencias.
    OPTIMIZADO para legibilidad universal.
    
    Args:
        df (pd.DataFrame): DataFrame con datos temporales
        x_col (str): Columna del eje X (tiempo)
        y_col (str): Columna del eje Y (valor)
        title (str): Título del gráfico
        y_title (str): Título del eje Y
        
    Returns:
        plotly.graph_objects.Figure: Figura de área configurada
    """
    if df.empty:
        return go.Figure()
    
    fig = px.area(
        df,
        x=x_col,
        y=y_col,
        title=title,
        color_discrete_sequence=[COLORS['health']],
        line_shape='spline'
    )
    
    fig.update_traces(
        mode='lines',
        line=dict(width=3),
        fillcolor=f"{COLORS['health']}40",  # Color con transparencia
        hovertemplate="<b>%{x}</b><br>" +
                     f"{y_title}: %{{y}}<br>" +
                     "<extra></extra>"
    )
    
    # Aplicar configuración universal
    fig = apply_universal_layout(fig, title)
    
    fig.update_layout(
        height=450,
        xaxis_title="Año",
        yaxis_title=y_title if y_title else y_col.replace('_', ' ').title()
    )
    
    return fig

def plot_bar_graduados(df_graduados):
    """
    Crea un gráfico de barras horizontales para graduados por área de conocimiento.
    Más legible que un donut cuando hay muchas categorías.
    OPTIMIZADO para legibilidad universal.
    
    Args:
        df_graduados (pd.DataFrame): DataFrame con datos de graduados
        
    Returns:
        plotly.graph_objects.Figure: Figura de barras configurada
    """
    if df_graduados.empty:
        return go.Figure()
    
    # Ordenar por número de graduados (de mayor a menor)
    df_sorted = df_graduados.sort_values('numero_de_graduados', ascending=True)
    
    fig = px.bar(
        df_sorted,
        x='numero_de_graduados',
        y='area_de_conocimiento',
        orientation='h',
        title='<b>🎓 Distribución de Graduados por Área de Conocimiento</b>',
        color='numero_de_graduados',
        color_continuous_scale='Viridis',
        text='numero_de_graduados'
    )
    
    fig.update_traces(
        texttemplate='%{text:,}',
        textposition='outside',
        textfont=dict(size=12, color=COLORS['text_dark'], family="Inter"),
        hovertemplate="<b>%{y}</b><br>" +
                     "Graduados: %{x:,}<br>" +
                     "<extra></extra>",
        marker=dict(line=dict(color='white', width=1))
    )
    
    # Aplicar configuración universal
    fig = apply_universal_layout(fig, "🎓 Distribución de Graduados por Área de Conocimiento")
    
    fig.update_layout(
        height=600,
        showlegend=False,
        xaxis_title="Número de Graduados",
        yaxis_title="Área de Conocimiento"
    )
    
    return fig

def plot_barras_empresas_moderno(df_empresarial):
    """
    Crea un gráfico de barras moderno para empresas por tamaño.
    OPTIMIZADO para legibilidad universal.
    
    Args:
        df_empresarial (pd.DataFrame): DataFrame con datos empresariales
        
    Returns:
        plotly.graph_objects.Figure: Figura de barras configurada
    """
    if df_empresarial.empty:
        return go.Figure()
    
    fig = px.bar(
        df_empresarial,
        x='tamaño_de_empresa',
        y='numero_de_empresas',
        title='🏢 Distribución de Empresas por Tamaño',
        color='numero_de_empresas',
        color_continuous_scale='Blues',
        text='numero_de_empresas'
    )
    
    fig.update_traces(
        texttemplate='%{text:,}',
        textposition='outside',
        textfont=dict(size=13, color=COLORS['text_dark'], family="Inter"),
        hovertemplate="<b>%{x}</b><br>" +
                     "Empresas: %{y:,}<br>" +
                     "<extra></extra>",
        marker=dict(line=dict(color='white', width=2))
    )
    
    # Aplicar configuración universal
    fig = apply_universal_layout(fig, "🏢 Distribución de Empresas por Tamaño")
    
    fig.update_layout(
        height=500,
        showlegend=False,
        xaxis_tickangle=-45,
        xaxis_title="Tamaño de Empresa",
        yaxis_title="Número de Empresas"
    )
    
    return fig

def plot_barras_municipios_horizontal(df_municipios, top_n=8):
    """
    Crea un gráfico de barras horizontales para municipios.
    
    Args:
        df_municipios (pd.DataFrame): DataFrame con datos de municipios
        top_n (int): Número de municipios a mostrar
        
    Returns:
        plotly.graph_objects.Figure: Figura de barras horizontales
    """
    if df_municipios.empty:
        return go.Figure()
    
    # Tomar los top N municipios
    df_top = df_municipios.head(top_n)
    
    fig = px.bar(
        df_top,
        x='numero_de_empresas',
        y='municipio',
        orientation='h',
        title=f'Top {top_n} Municipios por Número de Empresas',
        color='numero_de_empresas',
        color_continuous_scale='Oranges',
        text='numero_de_empresas'
    )
    
    fig.update_traces(
        texttemplate='%{text:,}',
        textposition='outside',
        textfont_size=11,
        hovertemplate="<b>%{y}</b><br>" +
                     "Empresas: %{x:,}<br>" +
                     "<extra></extra>"
    )
    
    fig.update_layout(
        height=400,
        font=dict(family="Inter"),
        xaxis_title="Número de Empresas",
        yaxis_title="",
        showlegend=False
    )
    
    return fig

def plot_piramide_poblacional(df_ciclo_vital):
    """
    Crea una pirámide poblacional horizontal para mostrar la estructura demográfica.
    Reemplaza el gráfico de dona para mejor storytelling demográfico.
    
    Args:
        df_ciclo_vital (pd.DataFrame): DataFrame con datos de ciclo vital
        
    Returns:
        plotly.graph_objects.Figure: Figura de pirámide poblacional
    """
    if df_ciclo_vital.empty:
        return go.Figure()
    
    # Ordenar por edad (de mayor a menor para crear forma de pirámide)
    age_order = [
        'Persona mayor 60 años y más',
        'Adultez 29-59 años', 
        'Juventud 18-28 años',
        'Adolescencia 12-17 años',
        'Infancia 6-11 años',
        'Primera infancia 0-5 años'
    ]
    
    # Reordenar DataFrame según el orden de edad
    df_ordered = df_ciclo_vital.copy()
    df_ordered['order'] = df_ordered['ciclo_vital'].apply(
        lambda x: age_order.index(x) if x in age_order else len(age_order)
    )
    df_ordered = df_ordered.sort_values('order')
    
    # Crear gráfico de barras horizontales
    fig = px.bar(
        df_ordered,
        x='poblacion',
        y='ciclo_vital',
        orientation='h',
        title='👥 Estructura Demográfica por Ciclo Vital',
        color='poblacion',
        color_continuous_scale=COLORS['corporate'][:6],
        text='poblacion',
        labels={'poblacion': 'Población', 'ciclo_vital': 'Grupo Etario'}
    )
    
    fig.update_traces(
        texttemplate='%{text:,.0f}',
        textposition='outside',
        textfont=dict(size=12, color=COLORS['text_dark']),
        hovertemplate="<b>%{y}</b><br>" +
                     "Población: %{x:,}<br>" +
                     "<extra></extra>",
        marker=dict(line=dict(color='white', width=1))
    )
    
    # Aplicar configuración universal
    fig = apply_universal_layout(fig, "👥 Estructura Demográfica por Ciclo Vital")
    
    fig.update_layout(
        height=500,
        showlegend=False,
        yaxis=dict(categoryorder='array', categoryarray=df_ordered['ciclo_vital'].tolist())
    )
    
    return fig

def plot_dona_ciclo_vital(df_ciclo_vital):
    """
    DEPRECADO: Usar plot_piramide_poblacional para mejor storytelling.
    Mantener por compatibilidad.
    """
    return plot_piramide_poblacional(df_ciclo_vital)

def plot_barras_seguridad(df_seguridad):
    """
    Crea un gráfico de barras para datos de seguridad.
    
    Args:
        df_seguridad (pd.DataFrame): DataFrame con datos de seguridad
        
    Returns:
        plotly.graph_objects.Figure: Figura de barras configurada
    """
    if df_seguridad.empty:
        return go.Figure()
    
    fig = px.bar(
        df_seguridad,
        x='delito',
        y='casos_2023',
        title='Casos Reportados por Tipo de Delito (2023)',
        color='casos_2023',
        color_continuous_scale='Reds',
        text='casos_2023'
    )
    
    fig.update_traces(
        texttemplate='%{text:,}',
        textposition='outside',
        textfont_size=11,
        hovertemplate="<b>%{x}</b><br>" +
                     "Casos 2023: %{y:,}<br>" +
                     "<extra></extra>"
    )
    
    fig.update_layout(
        height=500,
        font=dict(family="Inter"),
        xaxis_title="Tipo de Delito",
        yaxis_title="Número de Casos",
        showlegend=False,
        xaxis_tickangle=-45
    )
    
    return fig

def plot_lineas_dengue(df_morbilidad):
    """
    Crea un gráfico de líneas para casos de dengue.
    
    Args:
        df_morbilidad (pd.DataFrame): DataFrame con datos de morbilidad
        
    Returns:
        plotly.graph_objects.Figure: Figura de líneas configurada
    """
    if df_morbilidad.empty:
        return go.Figure()
    
    fig = px.line(
        df_morbilidad,
        x='año',
        y='casos_dengue',
        title='Evolución de Casos de Dengue por Año',
        markers=True,
        line_shape='spline'
    )
    
    fig.update_traces(
        line=dict(color=COLORS['warning'], width=3),
        marker=dict(size=8, color=COLORS['secondary'])
    )
    
    fig.update_layout(
        height=400,
        font=dict(family="Inter"),
        xaxis_title="Año",
        yaxis_title="Casos de Dengue",
        hovermode='x unified'
    )
    
    return fig

def plot_area_calidad_agua(df_agua):
    """
    Crea un gráfico de área para índice de calidad del agua.
    
    Args:
        df_agua (pd.DataFrame): DataFrame con datos de calidad del agua
        
    Returns:
        plotly.graph_objects.Figure: Figura de área configurada
    """
    if df_agua.empty:
        return go.Figure()
    
    fig = px.area(
        df_agua,
        x='año',
        y='indice_riesgo_calidad_agua',
        title='Índice de Riesgo de Calidad del Agua por Año',
        color_discrete_sequence=[COLORS['info']]
    )
    
    fig.update_layout(
        height=400,
        font=dict(family="Inter"),
        xaxis_title="Año",
        yaxis_title="Índice de Riesgo",
        hovermode='x unified'
    )
    
    return fig

def plot_dona_graduados(df_graduados):
    """
    Crea un gráfico de dona para graduados por área.
    
    Args:
        df_graduados (pd.DataFrame): DataFrame con datos de graduados
        
    Returns:
        plotly.graph_objects.Figure: Figura de dona configurada
    """
    if df_graduados.empty:
        return go.Figure()
    
    fig = px.pie(
        df_graduados,
        names='area_de_conocimiento',
        values='numero_de_graduados',
        title='Distribución de Graduados por Área de Conocimiento',
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_traces(
        textposition='outside',
        textinfo='percent+label',
        textfont_size=10,
        hovertemplate="<b>%{label}</b><br>" +
                     "Graduados: %{value:,}<br>" +
                     "Porcentaje: %{percent}<br>" +
                     "<extra></extra>"
    )
    
    fig.update_layout(
        height=500,
        font=dict(size=11, family="Inter"),
        showlegend=False
    )
    
    return fig

def plot_barras_desercion_municipios(df_desercion):
    """
    Crea un gráfico de barras horizontales para deserción por municipio.
    
    Args:
        df_desercion (pd.DataFrame): DataFrame con datos de deserción
        
    Returns:
        plotly.graph_objects.Figure: Figura de barras horizontales
    """
    if df_desercion.empty:
        return go.Figure()
    
    # Ordenar por tasa de deserción
    df_sorted = df_desercion.sort_values('tasa_desercion', ascending=True)
    
    fig = px.bar(
        df_sorted,
        x='tasa_desercion',
        y='municipio',
        orientation='h',
        title='Tasa de Deserción Escolar por Municipio (%)',
        color='tasa_desercion',
        color_continuous_scale='RdYlGn_r',  # Rojo para valores altos, verde para bajos
        text='tasa_desercion'
    )
    
    fig.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside',
        textfont_size=11,
        hovertemplate="<b>%{y}</b><br>" +
                     "Tasa de Deserción: %{x:.1f}%<br>" +
                     "<extra></extra>"
    )
    
    fig.update_layout(
        height=400,
        font=dict(family="Inter"),
        xaxis_title="Tasa de Deserción (%)",
        yaxis_title="",
        showlegend=False
    )
    
    return fig

def create_metric_chart(value, title, color=COLORS['primary'], height=200):
    """
    Crea un gráfico tipo gauge/métrica para KPIs.
    
    Args:
        value (float): Valor de la métrica
        title (str): Título de la métrica
        color (str): Color del gráfico
        height (int): Altura del gráfico
        
    Returns:
        plotly.graph_objects.Figure: Figura de gauge configurada
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 100], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=height,
        font=dict(family="Inter")
    )
    
    return fig