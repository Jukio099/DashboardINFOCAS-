"""
🏢 Tejido Empresarial de Casanare - Versión Modernizada
Análisis del ecosistema empresarial y distribución territorial
"""

import streamlit as st
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.loader import load_empresarial, load_empresas_municipio
from utils.plotting import plot_funnel_empresas, plot_barras_municipios_horizontal

# Configuración de la página
st.set_page_config(
    layout="wide", 
    page_title="🏢 Tejido Empresarial - Casanare",
    page_icon="🏢"
)

# 🎨 ESTILOS MODERNOS
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'warning': '#d62728',
    'light': '#e6f3ff'
}

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-header {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        font-family: 'Inter', sans-serif;
    }}
    
    .section-header {{
        background: linear-gradient(90deg, {COLORS['light']} 0%, white 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border-left: 4px solid {COLORS['primary']};
        margin: 2rem 0 1rem 0;
        font-family: 'Inter', sans-serif;
    }}
    
    .metric-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #f0f0f0;
        margin: 1rem 0;
        text-align: center;
    }}
    
    .highlight-number {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {COLORS['primary']};
        margin: 0;
    }}
    
    .highlight-label {{
        font-size: 1rem;
        color: #666;
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }}
    
    .insights-card {{
        background: linear-gradient(135deg, {COLORS['primary']}15 0%, {COLORS['secondary']}10 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid {COLORS['primary']};
        margin: 1rem 0;
    }}
    
    .municipio-card {{
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        border-left: 4px solid {COLORS['secondary']};
    }}
</style>
""", unsafe_allow_html=True)

# 🏢 HEADER
st.markdown("""
<div class="main-header">
    <h1>🏢 Tejido Empresarial de Casanare</h1>
    <h3>🚀 Ecosistema empresarial y oportunidades de negocio</h3>
</div>
""", unsafe_allow_html=True)

# 📊 CARGAR DATOS
@st.cache_data
def load_business_data():
    """Carga datos empresariales"""
    return {
        'empresas': load_empresarial(),
        'municipios': load_empresas_municipio()
    }

# Cargar datos
with st.spinner("🏢 Cargando datos empresariales..."):
    data = load_business_data()

df_empresas = data['empresas']
df_municipios = data['municipios']

if df_empresas.empty or df_municipios.empty:
    st.error("❌ No se pudieron cargar los datos empresariales.")
    st.stop()

# 📈 SECCIÓN 1: MÉTRICAS EMPRESARIALES CLAVE
st.markdown('<div class="section-header"><h2>📈 Indicadores del Tejido Empresarial</h2></div>', unsafe_allow_html=True)

# Calcular métricas
total_empresas = df_empresas['numero_de_empresas'].sum()
total_municipios = len(df_municipios)
municipio_lider = df_municipios.iloc[0]  # Primer municipio (mayor número)
concentracion_lider = (municipio_lider['numero_de_empresas'] / df_municipios['numero_de_empresas'].sum()) * 100

# Calcular densidad empresarial (asumiendo población)
poblacion_estimada = 481938  # De los datos generales
densidad_empresarial = (total_empresas / poblacion_estimada) * 1000

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🏪 Total de Empresas",
        value=f"{total_empresas:,}",
        delta="Empresas activas",
        help="Número total de empresas registradas en Casanare"
    )

with col2:
    st.metric(
        label="🌆 Municipios Activos",
        value=total_municipios,
        delta="Cobertura territorial",
        help="Municipios con registro empresarial"
    )

with col3:
    st.metric(
        label="👑 Municipio Líder",
        value=f"{concentracion_lider:.1f}%",
        delta=municipio_lider['municipio'],
        help="Concentración empresarial en el municipio principal"
    )

with col4:
    st.metric(
        label="📊 Densidad Empresarial",
        value=f"{densidad_empresarial:.1f}",
        delta="Por cada 1,000 hab.",
        help="Número de empresas por cada 1,000 habitantes"
    )

# 🏢 SECCIÓN 2: ANÁLISIS POR TAMAÑO DE EMPRESA
st.markdown('<div class="section-header"><h2>🏢 Distribución por Tamaño de Empresa</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    # Gráfico de barras mejorado
    # Gráfico de embudo - más narrativo para mostrar el "filtrado" empresarial
    fig_empresas = plot_funnel_empresas(df_empresas)
    st.plotly_chart(fig_empresas, use_container_width=True)

with col2:
    st.markdown("### 📊 Estructura Empresarial")
    
    # Análisis por tamaño
    for _, empresa in df_empresas.iterrows():
        porcentaje = (empresa['numero_de_empresas'] / total_empresas) * 100
        
        # Determinar color según tamaño
        if empresa['tamaño_de_empresa'] == 'Micro':
            color = COLORS['primary']
        elif empresa['tamaño_de_empresa'] == 'Pequeña':
            color = COLORS['secondary']
        elif empresa['tamaño_de_empresa'] == 'Mediana':
            color = COLORS['success']
        else:
            color = COLORS['warning']
        
        st.markdown(f"""
        <div class="metric-card">
            <p class="highlight-number" style="color: {color};">{empresa['numero_de_empresas']:,}</p>
            <p class="highlight-label">{empresa['tamaño_de_empresa']}: {porcentaje:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Análisis adicional
    microempresas_pct = (df_empresas[df_empresas['tamaño_de_empresa'] == 'Micro']['numero_de_empresas'].iloc[0] / total_empresas) * 100
    
    st.markdown("### 💡 Insights Clave")
    
    if microempresas_pct > 90:
        nivel_micro = "Muy Alto"
        color_micro = COLORS['warning']
    elif microempresas_pct > 80:
        nivel_micro = "Alto" 
        color_micro = COLORS['secondary']
    else:
        nivel_micro = "Moderado"
        color_micro = COLORS['success']
    
    st.markdown(f"""
    <div style="background: {color_micro}15; padding: 1rem; border-radius: 8px; border-left: 4px solid {color_micro};">
        <strong style="color: {color_micro};">Concentración de Microempresas: {nivel_micro}</strong><br>
        <small>{microempresas_pct:.1f}% del total son microempresas</small>
    </div>
    """, unsafe_allow_html=True)

# 🌆 SECCIÓN 3: ANÁLISIS TERRITORIAL
st.markdown('<div class="section-header"><h2>🌆 Distribución Territorial de Empresas</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    # Gráfico de municipios
    fig_municipios = plot_barras_municipios_horizontal(df_municipios, top_n=10)
    st.plotly_chart(fig_municipios, use_container_width=True)

with col2:
    st.markdown("### 🏆 Top 5 Municipios")
    
    top5_municipios = df_municipios.head(5)
    total_empresas_municipios = df_municipios['numero_de_empresas'].sum()
    
    for i, (_, municipio) in enumerate(top5_municipios.iterrows(), 1):
        participacion = (municipio['numero_de_empresas'] / total_empresas_municipios) * 100
        
        # Medallas para los primeros 3
        if i == 1:
            medal = "🥇"
            color = "#FFD700"
        elif i == 2:
            medal = "🥈"
            color = "#C0C0C0"
        elif i == 3:
            medal = "🥉"
            color = "#CD7F32"
        else:
            medal = f"#{i}"
            color = "#f0f0f0"
        
        st.markdown(f"""
        <div class="municipio-card" style="border-left-color: {color};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{medal} {municipio['municipio']}</strong><br>
                    <small style="color: #666;">{participacion:.1f}% del total</small>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 1.2rem; font-weight: bold; color: {COLORS['primary']};">
                        {municipio['numero_de_empresas']:,}
                    </span><br>
                    <small style="color: #666;">empresas</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Análisis de concentración territorial
    st.markdown("### 📍 Concentración Territorial")
    
    # Calcular índice de concentración (Top 3)
    top3_concentracion = top5_municipios.head(3)['numero_de_empresas'].sum()
    concentracion_pct = (top3_concentracion / total_empresas_municipios) * 100
    
    st.markdown(f"""
    <div class="metric-card">
        <p class="highlight-number">{concentracion_pct:.1f}%</p>
        <p class="highlight-label">Concentración Top 3 Municipios</p>
    </div>
    """, unsafe_allow_html=True)

# 📊 SECCIÓN 4: DATOS DETALLADOS
st.markdown('<div class="section-header"><h2>📊 Análisis Detallado</h2></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📈 Por Tamaño de Empresa", "🗺️ Por Municipio"])

with tab1:
    st.markdown("#### 🏢 Distribución Empresarial por Tamaño")
    
    # Preparar datos para mostrar
    df_empresas_display = df_empresas.copy()
    df_empresas_display['participacion_pct'] = (df_empresas_display['numero_de_empresas'] / total_empresas * 100).round(1)
    df_empresas_display['participacion_pct'] = df_empresas_display['participacion_pct'].map('{:.1f}%'.format)
    df_empresas_display['numero_de_empresas'] = df_empresas_display['numero_de_empresas'].map('{:,}'.format)
    
    # Renombrar columnas
    df_empresas_display.columns = ['Tamaño de Empresa', 'Número de Empresas', 'Porcentaje del Total', 'Participación (%)']
    
    st.dataframe(
        df_empresas_display[['Tamaño de Empresa', 'Número de Empresas', 'Participación (%)']],
        use_container_width=True,
        hide_index=True
    )
    
    # Análisis de estructura empresarial
    st.markdown("#### 📋 Análisis de Estructura")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **🔍 Características del Tejido Empresarial:**
        - **Predominio de Microempresas:** {microempresas_pct:.1f}% del total
        - **Base empresarial sólida:** {total_empresas:,} empresas activas
        - **Oportunidad de crecimiento:** Fortalecimiento de PYMES
        """)
    
    with col2:
        st.markdown(f"""
        **📊 Comparación Nacional:**
        - Colombia: ~95% microempresas (promedio)
        - Casanare: {microempresas_pct:.1f}% microempresas
        - **Análisis:** {"Por encima" if microempresas_pct > 95 else "Dentro"} del promedio nacional
        """)

with tab2:
    st.markdown("#### 🌆 Distribución Municipal de Empresas")
    
    # Preparar datos municipales
    df_municipios_display = df_municipios.copy()
    df_municipios_display['participacion_pct'] = (df_municipios_display['numero_de_empresas'] / total_empresas_municipios * 100).round(1)
    df_municipios_display['acumulado_pct'] = df_municipios_display['participacion_pct'].cumsum()
    df_municipios_display['ranking'] = range(1, len(df_municipios_display) + 1)
    
    # Formatear para visualización
    df_municipios_display['numero_de_empresas'] = df_municipios_display['numero_de_empresas'].map('{:,}'.format)
    df_municipios_display['participacion_pct'] = df_municipios_display['participacion_pct'].map('{:.1f}%'.format)
    df_municipios_display['acumulado_pct'] = df_municipios_display['acumulado_pct'].map('{:.1f}%'.format)
    
    # Seleccionar columnas para mostrar
    df_display = df_municipios_display[['ranking', 'municipio', 'numero_de_empresas', 'participacion_pct', 'acumulado_pct']]
    df_display.columns = ['Ranking', 'Municipio', 'N° Empresas', 'Participación (%)', 'Acumulado (%)']
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )

# 💡 SECCIÓN 5: INSIGHTS Y RECOMENDACIONES
st.markdown('<div class="section-header"><h2>💡 Insights y Oportunidades</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="insights-card">
        <h4 style="color: {COLORS['primary']}; margin-top: 0;">🎯 Fortalezas del Tejido Empresarial</h4>
        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
            <li><strong>Amplia base empresarial:</strong> {total_empresas:,} empresas activas</li>
            <li><strong>Cobertura territorial:</strong> Presencia en {total_municipios} municipios</li>
            <li><strong>Centro económico sólido:</strong> {municipio_lider['municipio']} como hub empresarial</li>
            <li><strong>Diversificación sectorial:</strong> Empresas en múltiples sectores</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="insights-card">
        <h4 style="color: {COLORS['secondary']}; margin-top: 0;">🚀 Oportunidades de Mejora</h4>
        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
            <li><strong>Crecimiento empresarial:</strong> Programas para escalar microempresas</li>
            <li><strong>Descentralización:</strong> Promover empresas en municipios menores</li>
            <li><strong>Innovación:</strong> Fomentar empresas de base tecnológica</li>
            <li><strong>Articulación:</strong> Crear clusters empresariales</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Estrategias específicas
st.markdown("### 📋 Estrategias Recomendadas")

estrategias = [
    {
        "titulo": "🎯 Fortalecimiento de PYMES",
        "descripcion": "Programas de capacitación, financiamiento y mentoría para microempresas que quieren crecer",
        "color": COLORS['success'],
        "prioridad": "Alta"
    },
    {
        "titulo": "🌐 Descentralización Empresarial", 
        "descripcion": "Incentivos para establecer empresas en municipios con menor concentración",
        "color": COLORS['secondary'],
        "prioridad": "Media"
    },
    {
        "titulo": "💡 Innovación y Tecnología",
        "descripcion": "Incubadoras de empresas y parques tecnológicos para nuevos emprendimientos",
        "color": COLORS['primary'],
        "prioridad": "Media"
    }
]

for estrategia in estrategias:
    st.markdown(f"""
    <div style="background: {estrategia['color']}15; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {estrategia['color']};">
        <div style="display: flex; justify-content: between; align-items: center;">
            <div style="flex-grow: 1;">
                <strong style="color: {estrategia['color']};">{estrategia['titulo']}</strong><br>
                <small>{estrategia['descripcion']}</small>
            </div>
            <div style="text-align: right; margin-left: 1rem;">
                <span style="background: {estrategia['color']}; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">
                    {estrategia['prioridad']}
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ✨ INSIGHTS Y PROPUESTAS DE ACCIÓN
st.markdown("---")
st.markdown("## ✨ **Insights y Propuestas de Acción**")

st.markdown(f"""
<div style="background: {COLORS['secondary']}15; padding: 2rem; border-radius: 15px; border-left: 5px solid {COLORS['secondary']}; margin: 2rem 0;">
    <h4 style="color: {COLORS['secondary']}; margin-top: 0;">🎯 Fortalecimiento del Tejido Empresarial</h4>
    
    <p><strong>Diagnóstico Clave:</strong></p>
    <p>El 94.7% del tejido empresarial está compuesto por microempresas, lo que indica un potencial enorme de crecimiento 
    pero también vulnerabilidad económica. La alta concentración en Yopal (52.1%) evidencia la necesidad de 
    descentralización territorial del desarrollo empresarial.</p>
    
    <p><strong>Propuestas Estratégicas:</strong></p>
    <ol>
        <li><strong>Programa de Escalamiento Empresarial:</strong> Crear incubadoras regionales que ayuden a 
        1,000 microempresas anuales a transitar hacia pequeñas empresas mediante capacitación, financiamiento y mentoría.</li>
        
        <li><strong>Descentralización Empresarial:</strong> Establecer centros de desarrollo empresarial en 
        Aguazul, Villanueva y Tauramena para reducir la concentración en Yopal y generar polos de desarrollo regional.</li>
        
        <li><strong>Clústers Sectoriales:</strong> Formar agrupaciones empresariales en agroindustria, turismo rural 
        y servicios tecnológicos que aprovechen las economías de escala y conocimiento compartido.</li>
        
        <li><strong>Simplificación Administrativa:</strong> Implementar ventanillas únicas digitales para 
        trámites empresariales y reducir los tiempos de formalización de empresas en un 50%.</li>
    </ol>
    
    <p><strong>Meta 2028:</strong> Aumentar las pequeñas y medianas empresas del 5.2% actual al 12% del total, 
    y lograr que el 25% de las nuevas empresas se establezcan fuera de Yopal.</p>
</div>
""", unsafe_allow_html=True)

# 🏛️ FOOTER
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, {COLORS['light']} 0%, white 100%); border-radius: 10px;">
    <p style="color: {COLORS['primary']}; font-size: 1.1rem; margin: 0;">
        🏢 <strong>Tejido Empresarial de Casanare</strong>
    </p>
    <p style="color: #666; margin: 0.5rem 0; font-size: 0.9rem;">
        <em>Impulsando el emprendimiento y la innovación empresarial</em>
    </p>
</div>
""", unsafe_allow_html=True)