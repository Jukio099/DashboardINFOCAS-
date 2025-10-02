"""
Visualizaciones académicas para sectores económicos
Gráfico: Mapa de Calor Ordenado (Ordered Heatmap)
"""

import altair as alt
import pandas as pd
from utils.loader_v3 import get_data_loader

def create_sectores_chart():
    """Crear gráfico de sectores económicos con Altair"""
    data_loader = get_data_loader()
    df = data_loader.get_sectores_economicos()
    
    if df.empty:
        return "<p>No hay datos disponibles</p>"
    
    # Crear mapa de calor ordenado
    chart = alt.Chart(df).mark_rect().add_selection(
        alt.selection_interval()
    ).encode(
        x=alt.X('sector_economico:N', 
                sort=alt.SortField(field='participacion_porcentual', order='descending'),
                title='Sector Económico'),
        y=alt.Y('participacion_porcentual:Q', title='Participación (%)'),
        color=alt.Color('participacion_porcentual:Q', 
                       scale=alt.Scale(scheme='viridis'),
                       title='Participación (%)'),
        tooltip=[
            alt.Tooltip('sector_economico:N', title='Sector'),
            alt.Tooltip('participacion_porcentual:Q', title='Participación (%)', format='.1f'),
            alt.Tooltip('valor_aproximado_cop_billones:Q', title='Valor (COP Billones)', format='.1f')
        ]
    ).properties(
        width=600,
        height=400,
        title={
            "text": "Composición del PIB por Sectores Económicos",
            "fontSize": 16,
            "fontWeight": "bold"
        }
    ).resolve_scale(
        color='independent'
    )
    
    # Agregar texto en las barras
    text = chart.mark_text(
        align='center',
        baseline='middle',
        color='white',
        fontWeight='bold'
    ).encode(
        text=alt.Text('participacion_porcentual:Q', format='.1f')
    )
    
    final_chart = (chart + text).resolve_scale(color='independent')
    
    return final_chart.to_html()
