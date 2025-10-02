"""
Visualizaciones académicas para graduados
Gráfico: Gráfico de Barras Radiales (Radial Bar Chart)
"""

import altair as alt
import pandas as pd
import numpy as np
from utils.loader_v3 import get_data_loader

def create_graduados_chart():
    """Crear gráfico de graduados con Altair"""
    data_loader = get_data_loader()
    df = data_loader.get_graduados_por_area()
    
    if df.empty:
        return "<p>No hay datos disponibles</p>"
    
    # Ordenar por número de graduados
    df = df.sort_values('numero_de_graduados', ascending=True)
    
    # Crear gráfico de barras radiales
    chart = alt.Chart(df).mark_arc(
        innerRadius=50,
        outerRadius=200
    ).encode(
        theta=alt.Theta('numero_de_graduados:Q', title='Número de Graduados'),
        radius=alt.Radius('numero_de_graduados:Q', scale=alt.Scale(type='sqrt')),
        color=alt.Color('area_de_conocimiento:N', 
                       scale=alt.Scale(scheme='category20'),
                       title='Área de Conocimiento'),
        tooltip=[
            alt.Tooltip('area_de_conocimiento:N', title='Área'),
            alt.Tooltip('numero_de_graduados:Q', title='Graduados', format=','),
            alt.Tooltip('porcentaje_del_total:Q', title='Porcentaje (%)', format='.1f')
        ]
    ).properties(
        width=600,
        height=600,
        title={
            "text": "Graduados por Área de Conocimiento",
            "fontSize": 16,
            "fontWeight": "bold"
        }
    )
    
    # Agregar etiquetas
    labels = chart.mark_text(
        align='center',
        baseline='middle',
        fontSize=12,
        fontWeight='bold'
    ).encode(
        text=alt.Text('area_de_conocimiento:N'),
        theta=alt.Theta('numero_de_graduados:Q'),
        radius=alt.Radius('numero_de_graduados:Q', scale=alt.Scale(type='sqrt'))
    )
    
    final_chart = chart + labels
    
    return final_chart.to_html()
