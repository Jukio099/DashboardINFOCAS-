"""
Módulo para la creación de visualizaciones con Plotly.
Contiene funciones específicas para cada tipo de gráfico utilizado en el dashboard.
"""

import plotly.express as px
import plotly.graph_objects as go


def plot_ranking_bars(df_ranking):
    """
    Crea un gráfico de barras horizontales para mostrar los rankings de competitividad.
    
    Args:
        df_ranking (pd.DataFrame): DataFrame con datos de ranking
        
    Returns:
        plotly.graph_objects.Figure: Figura de Plotly configurada
    """
    if df_ranking.empty:
        return go.Figure()
        
    fig = px.bar(
        df_ranking.sort_values('Valor'),
        x='Valor',
        y='Indicador',
        orientation='h',
        title='Desempeño en Pilares de Competitividad',
        text='Valor',
        labels={'Valor': 'Puntaje (0-10)', 'Indicador': ''}
    )
    
    fig.update_traces(
        texttemplate='%{text:.2f}', 
        textposition='outside', 
        marker_color='#0077B6'
    )
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    
    return fig


def plot_donut_sectores(df_sector):
    """
    Crea un gráfico de donut para mostrar la composición del PIB por sectores.
    
    Args:
        df_sector (pd.DataFrame): DataFrame con datos de sectores económicos
        
    Returns:
        plotly.graph_objects.Figure: Figura de Plotly configurada
    """
    if df_sector is None or df_sector.empty:
        return go.Figure()
        
    fig = px.pie(
        df_sector,
        names='Sector Económico',
        values='Participación Porcentual (%)',
        title='Participación de Sectores Económicos en el PIB',
        hole=0.4,  # Esto crea el agujero en el centro
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    
    fig.update_traces(
        textinfo='percent+label', 
        pull=[0.05, 0, 0, 0, 0, 0]
    )
    
    return fig


def plot_barras_empresas_tamaño(df_empresarial):
    """
    Crea un gráfico de barras para mostrar la distribución de empresas por tamaño.
    
    Args:
        df_empresarial (pd.DataFrame): DataFrame con datos empresariales
        
    Returns:
        plotly.graph_objects.Figure: Figura de Plotly configurada
    """
    if df_empresarial is None or df_empresarial.empty:
        return go.Figure()
        
    fig = px.bar(
        df_empresarial,
        x='Tamaño de Empresa',
        y='Número de Empresas',
        title='Número de Empresas por Tamaño',
        text='Número de Empresas',
        labels={'Número de Empresas': 'Cantidad', 'Tamaño de Empresa': 'Tamaño'}
    )
    
    fig.update_traces(marker_color='teal')
    
    return fig


def plot_barras_municipios(df_municipios):
    """
    Crea un gráfico de barras para mostrar la distribución de empresas por municipio.
    
    Args:
        df_municipios (pd.DataFrame): DataFrame con datos de municipios
        
    Returns:
        plotly.graph_objects.Figure: Figura de Plotly configurada
    """
    if df_municipios is None or df_municipios.empty:
        return go.Figure()
        
    fig = px.bar(
        df_municipios,
        x='Municipio',
        y='Número de Empresas',
        title='Top Municipios por Número de Empresas',
        text='Número de Empresas',
        labels={'Número de Empresas': 'Cantidad', 'Municipio': 'Municipio'}
    )
    
    fig.update_traces(marker_color='coral')
    
    return fig
