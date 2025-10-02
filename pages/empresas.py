"""
Visualizaciones académicas para tejido empresarial
Gráfico: Gráfico de Waffle (Waffle Chart)
"""

import altair as alt
import pandas as pd
import numpy as np
from utils.loader_v3 import get_data_loader

def create_empresas_chart():
    """Crear gráfico de empresas con Altair"""
    data_loader = get_data_loader()
    df = data_loader.get_empresas_por_tamano()
    
    if df.empty:
        return "<p>No hay datos disponibles</p>"
    
    # Crear gráfico de waffle
    # Primero, crear datos para el waffle
    waffle_data = []
    for _, row in df.iterrows():
        tamano = row['tamano_de_empresa']
        porcentaje = row['porcentaje_del_total']
        numero_empresas = row['numero_de_empresas']
        
        # Crear 100 cuadros para el waffle
        for i in range(int(porcentaje)):
            waffle_data.append({
                'tamano': tamano,
                'porcentaje': porcentaje,
                'numero_empresas': numero_empresas,
                'x': i % 10,
                'y': i // 10
            })
    
    waffle_df = pd.DataFrame(waffle_data)
    
    # Crear gráfico de waffle
    chart = alt.Chart(waffle_df).mark_rect(
        stroke='white',
        strokeWidth=1
    ).encode(
        x=alt.X('x:O', axis=None),
        y=alt.Y('y:O', axis=None),
        color=alt.Color('tamano:N', 
                       scale=alt.Scale(scheme='category20'),
                       title='Tamaño de Empresa'),
        tooltip=[
            alt.Tooltip('tamano:N', title='Tamaño'),
            alt.Tooltip('porcentaje:Q', title='Porcentaje (%)', format='.1f'),
            alt.Tooltip('numero_empresas:Q', title='Número de Empresas', format=',')
        ]
    ).properties(
        width=500,
        height=500,
        title={
            "text": "Distribución del Tejido Empresarial por Tamaño",
            "fontSize": 16,
            "fontWeight": "bold"
        }
    )
    
    return chart.to_html()
