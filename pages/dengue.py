"""
Visualizaciones académicas para dengue
Gráfico: Gráfico de Área con Líneas
"""

import altair as alt
import pandas as pd
from utils.loader_v3 import get_data_loader

def create_dengue_chart():
    """Crear gráfico de dengue con Altair"""
    data_loader = get_data_loader()
    df = data_loader.get_dengue_data()
    
    if df.empty:
        return "<p>No hay datos disponibles</p>"
    
    # Crear gráfico de área
    chart = alt.Chart(df).mark_area(
        line=True,
        point=True,
        opacity=0.7
    ).encode(
        x=alt.X('a_o:O', title='Año'),
        y=alt.Y('valor:Q', title='Número de Casos'),
        color=alt.value('#FF7F0E'),
        tooltip=[
            alt.Tooltip('a_o:O', title='Año'),
            alt.Tooltip('valor:Q', title='Casos', format=','),
            alt.Tooltip('indicador:N', title='Indicador')
        ]
    ).properties(
        width=600,
        height=400,
        title={
            "text": "Evolución de Casos de Dengue en Casanare",
            "fontSize": 16,
            "fontWeight": "bold"
        }
    )
    
    return chart.to_html()
