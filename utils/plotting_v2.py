"""
Sistema de visualización v2.0 - Gráficos Académicamente Correctos
Implementa las mejores prácticas de visualización de datos según principios académicos.

Principios aplicados:
1. Composición y Distribución: Treemap y Barras Horizontales Ordenadas
2. Comparación entre Categorías: Barras Horizontales con ordenamiento lógico
3. Datos Demográficos: Pirámide Poblacional
4. Series Temporales: Gráficos de Líneas con marcadores
5. Comparación de Rendimiento: Gráficos de Bala (Bullet Charts)
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional, Dict, Any, List
import numpy as np

# 🎨 PALETA DE COLORES CORPORATIVA CASANARE
COLORS = {
    'primary': '#1f77b4',        # Azul corporativo
    'secondary': '#ff7f0e',      # Naranja
    'success': '#2ca02c',        # Verde
    'warning': '#d62728',        # Rojo
    'info': '#9467bd',           # Púrpura
    'neutral': '#6c757d',       # Gris neutro
    'accent': '#17a2b8',         # Azul acento
    'light': '#f8f9fa',          # Gris claro
    'dark': '#343a40',           # Gris oscuro
    'text_dark': '#333333',      # Texto oscuro
    'corporate': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#17a2b8', '#6c757d']
}

# 🎨 CONFIGURACIÓN UNIVERSAL PARA GRÁFICOS
def apply_academic_layout(fig, title: str, subtitle: str = "", height: int = 500):
    """
    Aplica configuración académica para máxima legibilidad y profesionalismo.
    """
    fig.update_layout(
        # Fondos transparentes para adaptarse al tema
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        
        # Tipografía profesional
        font=dict(
            family="Inter, Arial, sans-serif",
            size=12,
            color=COLORS['text_dark']
        ),
        
        # Título principal y subtítulo
        title=dict(
            text=f"<b>{title}</b><br><span style='font-size:11px;color:#666'>{subtitle}</span>",
            x=0.5,
            xanchor='center',
            font=dict(size=16, color=COLORS['text_dark'], family="Inter"),
            pad=dict(t=20, b=20)
        ),
        
        # Ejes limpios y profesionales
        xaxis=dict(
            gridcolor='rgba(128,128,128,0.1)',
            tickfont=dict(color=COLORS['text_dark'], size=11),
            title=dict(font=dict(color=COLORS['text_dark'], size=12)),
            showline=True,
            linecolor='rgba(128,128,128,0.3)',
            zeroline=False
        ),
        yaxis=dict(
            gridcolor='rgba(128,128,128,0.1)',
            tickfont=dict(color=COLORS['text_dark'], size=11),
            title=dict(font=dict(color=COLORS['text_dark'], size=12)),
            showline=True,
            linecolor='rgba(128,128,128,0.3)',
            zeroline=False
        ),
        
        # Leyenda profesional
        legend=dict(
            font=dict(color=COLORS['text_dark'], size=11),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(128,128,128,0.3)',
            borderwidth=1
        ),
        
        # Altura y márgenes
        height=height,
        margin=dict(t=80, l=60, r=60, b=60),
        
        # Eliminar elementos innecesarios
        showlegend=True
    )
    return fig


# 1. COMPOSICIÓN Y DISTRIBUCIÓN (Parte-a-Todo)

def plot_sector_economico_academic(df_sectores: pd.DataFrame) -> go.Figure:
    """
    Gráfico académicamente correcto para composición económica.
    Usa barras horizontales ordenadas para comparación precisa.
    """
    if df_sectores.empty:
        return go.Figure()
    
    # Filtrar datos válidos y excluir total
    df_clean = df_sectores[
        (df_sectores['sector_economico'] != 'Total') & 
        (df_sectores['participacion_porcentual'].notna()) &
        (df_sectores['participacion_porcentual'] > 0)
    ].copy()
    
    if df_clean.empty:
        return go.Figure()
    
    # Ordenar de mayor a menor para revelar estructura
    df_clean = df_clean.sort_values('participacion_porcentual', ascending=True)
    
    # Crear gráfico de barras horizontales
    fig = go.Figure()
    
    # Color con propósito: neutro para todas, acento para el líder
    colors = [COLORS['accent'] if i == 0 else COLORS['neutral'] 
              for i in range(len(df_clean))]
    
    fig.add_trace(go.Bar(
        y=df_clean['sector_economico'],
        x=df_clean['participacion_porcentual'],
        orientation='h',
        marker=dict(color=colors),
        text=[f"{val:.1f}%" for val in df_clean['participacion_porcentual']],
        textposition='outside',
        textfont=dict(size=11, color=COLORS['text_dark']),
        hovertemplate="<b>%{y}</b><br>" +
                     "Participación: %{x:.1f}%<br>" +
                     "<extra></extra>",
        showlegend=False
    ))
    
    # Aplicar layout académico
    fig = apply_academic_layout(
        fig, 
        "El 50.4% de la Economía de Casanare se Concentra en la Explotación Minera",
        "Participación porcentual de sectores en el PIB departamental",
        height=600
    )
    
    # Configuración específica para barras horizontales
    fig.update_layout(
        xaxis_title="Participación en el PIB (%)",
        yaxis_title="",
        xaxis=dict(range=[0, max(df_clean['participacion_porcentual']) * 1.1]),
        yaxis=dict(categoryorder='array', categoryarray=df_clean['sector_economico'].tolist())
    )
    
    return fig


def plot_empresas_tamaño_academic(df_empresas: pd.DataFrame) -> go.Figure:
    """
    Gráfico académicamente correcto para distribución empresarial.
    Revela la estructura del tejido empresarial.
    """
    if df_empresas.empty:
        return go.Figure()
    
    # Filtrar y ordenar
    df_clean = df_empresas[df_empresas['tamaño_de_empresa'] != 'Total'].copy()
    df_clean = df_clean.sort_values('numero_de_empresas', ascending=True)
    
    # Crear gráfico
    fig = go.Figure()
    
    # Color con propósito: destacar microempresas
    colors = []
    for i, row in df_clean.iterrows():
        if row['tamaño_de_empresa'] == 'Micro':
            colors.append(COLORS['accent'])
        else:
            colors.append(COLORS['neutral'])
    
    fig.add_trace(go.Bar(
        y=df_clean['tamaño_de_empresa'],
        x=df_clean['numero_de_empresas'],
        orientation='h',
        marker=dict(color=colors),
        text=[f"{val:,.0f}" for val in df_clean['numero_de_empresas']],
        textposition='outside',
        textfont=dict(size=11, color=COLORS['text_dark']),
        hovertemplate="<b>%{y}</b><br>" +
                     "Empresas: %{x:,.0f}<br>" +
                     "<extra></extra>",
        showlegend=False
    ))
    
    # Aplicar layout académico
    fig = apply_academic_layout(
        fig,
        "El 94.7% del Tejido Empresarial de Casanare son Microempresas",
        "Distribución del número de empresas por tamaño",
        height=400
    )
    
    fig.update_layout(
        xaxis_title="Número de Empresas",
        yaxis_title="",
        xaxis=dict(range=[0, max(df_clean['numero_de_empresas']) * 1.1])
    )
    
    return fig


# 2. COMPARACIÓN ENTRE CATEGORÍAS

def plot_municipios_empresas_academic(df_municipios: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """
    Gráfico académicamente correcto para comparación de municipios.
    Ordenado para identificar rápidamente los líderes.
    """
    if df_municipios.empty:
        return go.Figure()
    
    # Tomar top N y ordenar
    df_top = df_municipios.head(top_n).copy()
    df_top = df_top.sort_values('numero_de_empresas', ascending=True)
    
    fig = go.Figure()
    
    # Color con propósito: destacar Yopal
    colors = []
    for i, row in df_top.iterrows():
        if row['municipio'] == 'Yopal':
            colors.append(COLORS['accent'])
        else:
            colors.append(COLORS['neutral'])
    
    fig.add_trace(go.Bar(
        y=df_top['municipio'],
        x=df_top['numero_de_empresas'],
        orientation='h',
        marker=dict(color=colors),
        text=[f"{val:,.0f}" for val in df_top['numero_de_empresas']],
        textposition='outside',
        textfont=dict(size=11, color=COLORS['text_dark']),
        hovertemplate="<b>%{y}</b><br>" +
                     "Empresas: %{x:,.0f}<br>" +
                     "<extra></extra>",
        showlegend=False
    ))
    
    # Aplicar layout académico
    fig = apply_academic_layout(
        fig,
        "Yopal Concentra el 51% de las Empresas del Departamento",
        f"Top {top_n} municipios por número de empresas registradas",
        height=500
    )
    
    fig.update_layout(
        xaxis_title="Número de Empresas",
        yaxis_title="",
        xaxis=dict(range=[0, max(df_top['numero_de_empresas']) * 1.1])
    )
    
    return fig


def plot_delitos_seguridad_academic(df_seguridad: pd.DataFrame) -> go.Figure:
    """
    Gráfico académicamente correcto para comparación de delitos.
    """
    if df_seguridad.empty:
        return go.Figure()
    
    # Ordenar por número de casos
    df_clean = df_seguridad.sort_values('casos_2023', ascending=True)
    
    fig = go.Figure()
    
    # Color con propósito: escala de gravedad
    colors = []
    for i, row in df_clean.iterrows():
        if row['casos_2023'] > 500:
            colors.append(COLORS['warning'])
        elif row['casos_2023'] > 100:
            colors.append(COLORS['secondary'])
        else:
            colors.append(COLORS['neutral'])
    
    fig.add_trace(go.Bar(
        y=df_clean['delito'],
        x=df_clean['casos_2023'],
        orientation='h',
        marker=dict(color=colors),
        text=[f"{val:,.0f}" for val in df_clean['casos_2023']],
        textposition='outside',
        textfont=dict(size=11, color=COLORS['text_dark']),
        hovertemplate="<b>%{y}</b><br>" +
                     "Casos 2023: %{x:,.0f}<br>" +
                     "<extra></extra>",
        showlegend=False
    ))
    
    # Aplicar layout académico
    fig = apply_academic_layout(
        fig,
        "Hurto a Personas es el Delito Más Frecuente en Casanare",
        "Casos reportados por tipo de delito en 2023",
        height=400
    )
    
    fig.update_layout(
        xaxis_title="Número de Casos",
        yaxis_title="",
        xaxis=dict(range=[0, max(df_clean['casos_2023']) * 1.1])
    )
    
    return fig


# 3. DATOS DEMOGRÁFICOS - PIRÁMIDE POBLACIONAL

def plot_piramide_poblacional_academic(df_ciclo: pd.DataFrame) -> go.Figure:
    """
    Pirámide poblacional académicamente correcta.
    Estándar de oro en demografía.
    """
    if df_ciclo.empty:
        return go.Figure()
    
    # Ordenar por edad (jóvenes abajo, mayores arriba)
    age_order = [
        'Primera infancia 0-5 años',
        'Infancia 6-11 años', 
        'Adolescencia 12-17 años',
        'Juventud 18-28 años',
        'Adultez 29-59 años',
        'Persona mayor 60 años y más'
    ]
    
    # Reordenar DataFrame
    df_ordered = df_ciclo.copy()
    df_ordered['order'] = df_ordered['ciclo_vital'].apply(
        lambda x: age_order.index(x) if x in age_order else len(age_order)
    )
    df_ordered = df_ordered.sort_values('order')
    
    # Crear gráfico de barras horizontales (pirámide)
    fig = go.Figure()
    
    # Colores por grupo etario
    colors = [COLORS['corporate'][i % len(COLORS['corporate'])] 
              for i in range(len(df_ordered))]
    
    fig.add_trace(go.Bar(
        y=df_ordered['ciclo_vital'],
        x=df_ordered['poblacion'],
        orientation='h',
        marker=dict(color=colors),
        text=[f"{val:,.0f}" for val in df_ordered['poblacion']],
        textposition='outside',
        textfont=dict(size=11, color=COLORS['text_dark']),
        hovertemplate="<b>%{y}</b><br>" +
                     "Población: %{x:,.0f}<br>" +
                     "<extra></extra>",
        showlegend=False
    ))
    
    # Aplicar layout académico
    fig = apply_academic_layout(
        fig,
        "Estructura Demográfica de Casanare por Ciclo Vital, 2025",
        "Una base poblacional joven con un significativo cohorte en edad productiva",
        height=600
    )
    
    fig.update_layout(
        xaxis_title="Población",
        yaxis_title="",
        xaxis=dict(range=[0, max(df_ordered['poblacion']) * 1.1]),
        yaxis=dict(categoryorder='array', categoryarray=df_ordered['ciclo_vital'].tolist())
    )
    
    return fig


# 4. SERIES TEMPORALES

def plot_evolucion_dengue_academic(df_morbilidad: pd.DataFrame) -> go.Figure:
    """
    Gráfico de líneas académicamente correcto para series temporales.
    """
    if df_morbilidad.empty:
        return go.Figure()
    
    # Filtrar datos de dengue
    df_dengue = df_morbilidad[df_morbilidad['indicador'].str.contains('dengue', case=False, na=False)].copy()
    
    if df_dengue.empty:
        return go.Figure()
    
    # Ordenar por año
    df_dengue = df_dengue.sort_values('año')
    
    fig = go.Figure()
    
    # Línea con marcadores
    fig.add_trace(go.Scatter(
        x=df_dengue['año'],
        y=df_dengue['valor'],
        mode='lines+markers',
        line=dict(color=COLORS['warning'], width=3),
        marker=dict(size=8, color=COLORS['warning']),
        name='Casos de Dengue',
        hovertemplate="<b>Año: %{x}</b><br>" +
                     "Casos: %{y:,.0f}<br>" +
                     "<extra></extra>"
    ))
    
    # Aplicar layout académico
    fig = apply_academic_layout(
        fig,
        "Evolución de Casos de Dengue en Casanare",
        "Tendencia de casos reportados por año",
        height=500
    )
    
    fig.update_layout(
        xaxis_title="Año",
        yaxis_title="Número de Casos",
        xaxis=dict(tickmode='linear', dtick=1),
        yaxis=dict(range=[0, max(df_dengue['valor']) * 1.1])
    )
    
    # Anotar picos si existen
    max_cases = df_dengue['valor'].max()
    max_year = df_dengue[df_dengue['valor'] == max_cases]['año'].iloc[0]
    
    if max_cases > df_dengue['valor'].mean() * 1.5:  # Si hay un pico significativo
        fig.add_annotation(
            x=max_year,
            y=max_cases,
            text=f"Pico: {max_cases:,.0f} casos",
            showarrow=True,
            arrowhead=2,
            arrowcolor=COLORS['warning'],
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor=COLORS['warning']
        )
    
    return fig


# 5. COMPARACIÓN DE RENDIMIENTO - GRÁFICO DE BALA

def plot_bullet_chart_academic(data: Dict[str, float], title: str) -> go.Figure:
    """
    Gráfico de bala académicamente correcto para comparar rendimiento.
    """
    fig = go.Figure()
    
    # Bandas de rendimiento (ejemplo)
    poor_range = [0, data.get('target', 100) * 0.5]
    good_range = [data.get('target', 100) * 0.5, data.get('target', 100) * 0.8]
    excellent_range = [data.get('target', 100) * 0.8, data.get('target', 100) * 1.2]
    
    # Agregar bandas de fondo
    fig.add_trace(go.Bar(
        y=['Rendimiento'],
        x=[poor_range[1] - poor_range[0]],
        base=[poor_range[0]],
        marker=dict(color='rgba(220, 53, 69, 0.3)'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Bar(
        y=['Rendimiento'],
        x=[good_range[1] - good_range[0]],
        base=[good_range[0]],
        marker=dict(color='rgba(255, 193, 7, 0.3)'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Bar(
        y=['Rendimiento'],
        x=[excellent_range[1] - excellent_range[0]],
        base=[excellent_range[0]],
        marker=dict(color='rgba(40, 167, 69, 0.3)'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Barra principal (valor actual)
    fig.add_trace(go.Bar(
        y=['Rendimiento'],
        x=[data.get('current', 0)],
        marker=dict(color=COLORS['primary']),
        name='Valor Actual',
        hovertemplate="<b>Valor Actual</b><br>" +
                     "Valor: %{x}<br>" +
                     "<extra></extra>"
    ))
    
    # Línea de objetivo
    fig.add_trace(go.Scatter(
        x=[data.get('target', 0)],
        y=['Rendimiento'],
        mode='markers',
        marker=dict(symbol='line-ns', size=20, color=COLORS['warning']),
        name='Objetivo',
        hovertemplate="<b>Objetivo</b><br>" +
                     "Valor: %{x}<br>" +
                     "<extra></extra>"
    ))
    
    # Aplicar layout académico
    fig = apply_academic_layout(
        fig,
        title,
        "Comparación de rendimiento actual vs. objetivo",
        height=300
    )
    
    fig.update_layout(
        xaxis_title="Valor",
        yaxis_title="",
        xaxis=dict(range=[0, max(data.get('current', 0), data.get('target', 0)) * 1.2])
    )
    
    return fig


# FUNCIONES DE UTILIDAD

def create_dashboard_summary_plot(data_summary: Dict[str, Any]) -> go.Figure:
    """
    Crea un gráfico de resumen para el dashboard principal.
    """
    # Crear un gráfico de indicadores (gauges) para KPIs principales
    fig = go.Figure()
    
    # Agregar indicadores para KPIs clave
    kpis = data_summary.get('kpis', {})
    
    if kpis:
        # Crear subplots para múltiples indicadores
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]],
            subplot_titles=["Población 2025", "PIB 2023", "Puntaje IDC", "Ranking IDC"]
        )
        
        # Población
        fig.add_trace(go.Indicator(
            mode="number",
            value=kpis.get('poblacion_2025', 0),
            title={"text": "Población<br><span style='font-size:0.8em'>Habitantes</span>"},
            number={'font': {'size': 40}}
        ), row=1, col=1)
        
        # PIB
        pib_billones = kpis.get('pib_2023', 0) / 1000000
        fig.add_trace(go.Indicator(
            mode="number",
            value=pib_billones,
            title={"text": "PIB<br><span style='font-size:0.8em'>Billones COP</span>"},
            number={'font': {'size': 40}, 'suffix': 'B'}
        ), row=1, col=2)
        
        # Puntaje IDC
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=kpis.get('puntaje_idc', 0),
            domain={'x': [0, 1], 'y': [0, 1]},
            title={"text": "Puntaje IDC<br><span style='font-size:0.8em'>/10</span>"},
            gauge={'axis': {'range': [None, 10]},
                   'bar': {'color': COLORS['primary']},
                   'steps': [{'range': [0, 5], 'color': "lightgray"},
                            {'range': [5, 10], 'color': "gray"}]}
        ), row=2, col=1)
        
        # Ranking
        fig.add_trace(go.Indicator(
            mode="number",
            value=kpis.get('ranking_idc', 0),
            title={"text": "Ranking Nacional<br><span style='font-size:0.8em'>/32</span>"},
            number={'font': {'size': 40}, 'prefix': '#'}
        ), row=2, col=2)
    
    fig.update_layout(
        height=600,
        title="Indicadores Clave de Competitividad de Casanare",
        font=dict(family="Inter", size=12)
    )
    
    return fig
