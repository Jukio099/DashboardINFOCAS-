"""
Página de Análisis del Perfil Económico
Muestra la composición del PIB departamental por sectores económicos.
"""

import streamlit as st
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.loader import load_all_data
from utils.plotting import plot_donut_sectores

# Configuración de la página
st.set_page_config(
    layout="wide", 
    page_title="Perfil Económico - Dashboard Casanare"
)

# --- CONTENIDO DE LA PÁGINA ---
st.header("📊 Perfil Económico de Casanare")
st.markdown("Análisis detallado de la composición del Producto Interno Bruto departamental.")

# Cargar datos
data = load_all_data()
df_sector = data.get('sector')

if df_sector is not None:
    # Gráfico principal: Composición del PIB
    st.subheader("Composición del PIB Departamental")
    
    fig_donut = plot_donut_sectores(df_sector)
    st.plotly_chart(fig_donut, use_container_width=True)
    
    # Datos detallados
    st.subheader("Datos Detallados por Sector")
    
    # Mostrar tabla con información adicional
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(
            df_sector,
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        st.metric(
            "Total Sectores", 
            len(df_sector),
            help="Número total de sectores económicos analizados"
        )
        
        # Estadísticas adicionales
        if 'Participación Porcentual (%)' in df_sector.columns:
            max_sector = df_sector.loc[df_sector['Participación Porcentual (%)'].idxmax()]
            st.metric(
                "Sector Principal", 
                f"{max_sector['Sector Económico'][:20]}...",
                f"{max_sector['Participación Porcentual (%)']:.1f}%",
                help="Sector con mayor participación en el PIB"
            )

else:
    st.error("No se pudieron cargar los datos del perfil económico.")
    st.info("💡 **Tip**: Verifica que el archivo 'Indicadores generalidades - Sector Economico.csv' esté disponible.")

# --- INFORMACIÓN ADICIONAL ---
st.markdown("---")
st.info("""
**📊 Interpretación del Perfil Económico:**

- **Sectores Primarios**: Agricultura, ganadería, silvicultura y pesca
- **Sectores Secundarios**: Industria manufacturera, construcción, minería
- **Sectores Terciarios**: Comercio, servicios, transporte, turismo

El análisis de la composición del PIB permite identificar las fortalezas económicas del departamento y las oportunidades de diversificación.
""")
