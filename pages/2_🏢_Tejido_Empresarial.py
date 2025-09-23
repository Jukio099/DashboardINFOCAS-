"""
Página de Análisis del Tejido Empresarial
Muestra la distribución de empresas por tamaño y ubicación geográfica.
"""

import streamlit as st
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.loader import load_all_data
from utils.plotting import plot_barras_empresas_tamaño, plot_barras_municipios

# Configuración de la página
st.set_page_config(
    layout="wide", 
    page_title="Tejido Empresarial - Dashboard Casanare"
)

# --- CONTENIDO DE LA PÁGINA ---
st.header("🏢 Tejido Empresarial de Casanare")
st.markdown("Análisis de la estructura empresarial del departamento por tamaño y distribución geográfica.")

# Cargar datos
data = load_all_data()
df_empresarial = data.get('empresarial')
df_municipios = data.get('municipios')

if df_empresarial is not None and df_municipios is not None:
    # Métricas generales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_empresas = df_empresarial['Número de Empresas'].sum()
        st.metric("Total Empresas", f"{total_empresas:,}")
    
    with col2:
        total_municipios = len(df_municipios)
        st.metric("Municipios Analizados", total_municipios)
    
    with col3:
        if not df_municipios.empty:
            municipio_principal = df_municipios.loc[df_municipios['Número de Empresas'].idxmax()]
            st.metric(
                "Municipio Principal", 
                municipio_principal['Municipio'],
                f"{municipio_principal['Número de Empresas']:,} empresas"
            )

    st.markdown("---")
    
    # Análisis por tamaño de empresa
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribución por Tamaño de Empresa")
        
        fig_tamaño = plot_barras_empresas_tamaño(df_empresarial)
        st.plotly_chart(fig_tamaño, use_container_width=True)
        
        # Análisis adicional del tamaño
        if not df_empresarial.empty:
            st.caption("**Análisis por Tamaño:**")
            for _, row in df_empresarial.iterrows():
                porcentaje = (row['Número de Empresas'] / total_empresas) * 100
                st.write(f"• **{row['Tamaño de Empresa']}**: {porcentaje:.1f}% del total")

    with col2:
        st.subheader("Distribución por Municipio")
        
        fig_municipios = plot_barras_municipios(df_municipios)
        st.plotly_chart(fig_municipios, use_container_width=True)
        
        # Top 3 municipios
        if not df_municipios.empty:
            st.caption("**Top 3 Municipios:**")
            top_municipios = df_municipios.nlargest(3, 'Número de Empresas')
            for i, (_, row) in enumerate(top_municipios.iterrows(), 1):
                st.write(f"{i}. **{row['Municipio']}**: {row['Número de Empresas']:,} empresas")

    # Datos detallados
    st.markdown("---")
    st.subheader("Datos Detallados")
    
    tab1, tab2 = st.tabs(["📊 Por Tamaño", "🏢 Por Municipio"])
    
    with tab1:
        st.dataframe(
            df_empresarial,
            use_container_width=True,
            hide_index=True
        )
    
    with tab2:
        st.dataframe(
            df_municipios,
            use_container_width=True,
            hide_index=True
        )

else:
    st.error("No se pudieron cargar los datos del tejido empresarial.")
    st.info("""
    💡 **Tip**: Verifica que los siguientes archivos estén disponibles:
    - 'Indicadores generalidades - Empresarial.csv'
    - 'Indicadores generalidades - Numero de empresas por municipio.csv'
    """)

# --- INFORMACIÓN ADICIONAL ---
st.markdown("---")
st.info("""
**🏢 Clasificación por Tamaño de Empresa:**

- **Microempresas**: 1-10 empleados
- **Pequeñas**: 11-50 empleados  
- **Medianas**: 51-200 empleados
- **Grandes**: Más de 200 empleados

El tejido empresarial es fundamental para el desarrollo económico local y la generación de empleo en el departamento.
""")
