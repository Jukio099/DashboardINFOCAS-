"""
📊 Perfil Económico de Casanare - Versión Modernizada
Análisis detallado de sectores económicos y competitividad
"""

import streamlit as st
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.loader import load_sector_economico, load_generalidades
from utils.plotting import plot_treemap_sectores_mejorado

# Configuración de la página
st.set_page_config(
    layout="wide", 
    page_title="📊 Perfil Económico - Casanare",
    page_icon="📊"
)

# 🎨 ESTILOS MODERNOS
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
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
        margin: 0;
        font-weight: 500;
    }}
    
    .insights-card {{
        background: linear-gradient(135deg, {COLORS['primary']}15 0%, {COLORS['secondary']}10 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid {COLORS['primary']};
        margin: 1rem 0;
    }}
</style>
""", unsafe_allow_html=True)

# 📊 HEADER
st.markdown("""
<div class="main-header">
    <h1>📊 Perfil Económico de Casanare</h1>
    <h3>💼 Estructura productiva y oportunidades de crecimiento</h3>
</div>
""", unsafe_allow_html=True)

# 📊 CARGAR DATOS
@st.cache_data
def load_economic_data():
    """Carga datos económicos"""
    return {
        'sectores': load_sector_economico(),
        'generalidades': load_generalidades()
    }

# Cargar datos
with st.spinner("📈 Cargando datos económicos..."):
    data = load_economic_data()

df_sectores = data['sectores']
df_general = data['generalidades']

if df_sectores.empty:
    st.error("❌ No se pudieron cargar los datos de sectores económicos.")
    st.stop()

# 💰 SECCIÓN 1: MÉTRICAS ECONÓMICAS CLAVE
st.markdown('<div class="section-header"><h2>💰 Indicadores Económicos Clave</h2></div>', unsafe_allow_html=True)

# Calcular métricas
total_sectores = len(df_sectores)
sector_principal = df_sectores.loc[df_sectores['participacion_porcentual'].idxmax()]
pib_estimado = df_sectores['valor_aproximado_cop_billones'].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🎯 Sectores Analizados",
        value=total_sectores,
        delta="Diversificación sectorial",
        help="Número de sectores económicos principales"
    )

with col2:
    st.metric(
        label="🏆 Sector Líder",
        value=f"{sector_principal['participacion_porcentual']:.1f}%",
        delta=sector_principal['sector_economico'],
        help="Sector con mayor participación en el PIB"
    )

with col3:
    st.metric(
        label="💸 PIB Estimado",
        value=f"${pib_estimado:.1f}B COP",
        delta="Valor agregado total",
        help="Producto Interno Bruto estimado en billones"
    )

with col4:
    # Calcular concentración económica (top 3 sectores)
    top3_participacion = df_sectores.nlargest(3, 'participacion_porcentual')['participacion_porcentual'].sum()
    st.metric(
        label="📊 Concentración Top 3",
        value=f"{top3_participacion:.1f}%",
        delta="Diversificación económica",
        delta_color="inverse",
        help="Participación de los 3 sectores principales"
    )

# 🌳 SECCIÓN 2: TREEMAP DE SECTORES ECONÓMICOS
st.markdown('<div class="section-header"><h2>🌳 Composición Económica por Sectores</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2.5, 1])

with col1:
    # Treemap mejorado - colores más vivos y datos correctos
    fig_treemap = plot_treemap_sectores_mejorado(df_sectores)
    st.plotly_chart(fig_treemap, use_container_width=True)

with col2:
    st.markdown("### 📈 Top 5 Sectores")
    
    top5_sectores = df_sectores.nlargest(5, 'participacion_porcentual')
    
    for i, (_, sector) in enumerate(top5_sectores.iterrows(), 1):
        # Determinar color según posición
        if i == 1:
            badge_color = "#FFD700"  # Oro
        elif i == 2:
            badge_color = "#C0C0C0"  # Plata
        elif i == 3:
            badge_color = "#CD7F32"  # Bronce
        else:
            badge_color = "#f0f0f0"  # Gris claro
            
        st.markdown(f"""
        <div style="background: {badge_color}20; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid {badge_color};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>#{i} {sector['sector_economico']}</strong><br>
                    <small style="color: #666;">PIB: ${sector['valor_aproximado_cop_billones']:.1f}B COP</small>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 1.2rem; font-weight: bold; color: {COLORS['primary']};">
                        {sector['participacion_porcentual']:.1f}%
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Métricas adicionales
    st.markdown("### 📊 Análisis de Concentración")
    
    # Índice de Herfindahl-Hirschman (HHI) para medir concentración
    hhi = sum((df_sectores['participacion_porcentual'] / 100) ** 2) * 10000
    
    if hhi < 1500:
        concentracion = "Baja"
        color_hhi = COLORS['success']
    elif hhi < 2500:
        concentracion = "Moderada"
        color_hhi = COLORS['secondary']
    else:
        concentracion = "Alta"
        color_hhi = "#d62728"
    
    st.markdown(f"""
    <div class="metric-card">
        <p class="highlight-number" style="color: {color_hhi};">{hhi:.0f}</p>
        <p class="highlight-label">Índice HHI - Concentración {concentracion}</p>
    </div>
    """, unsafe_allow_html=True)

# 📋 SECCIÓN 3: ANÁLISIS DETALLADO
st.markdown('<div class="section-header"><h2>📋 Análisis Sectorial Detallado</h2></div>', unsafe_allow_html=True)

# Tabla interactiva con datos
with st.expander("📊 Ver datos completos por sector", expanded=False):
    # Agregar columnas calculadas
    df_display = df_sectores.copy()
    df_display['participacion_acumulada'] = df_display['participacion_porcentual'].cumsum()
    df_display['ranking'] = range(1, len(df_display) + 1)
    
    # Formatear columnas
    df_display['participacion_porcentual'] = df_display['participacion_porcentual'].map('{:.1f}%'.format)
    df_display['participacion_acumulada'] = df_display['participacion_acumulada'].map('{:.1f}%'.format)
    df_display['valor_aproximado_cop_billones'] = df_display['valor_aproximado_cop_billones'].map('${:.1f}B'.format)
    
    # Renombrar columnas para mostrar
    df_display = df_display[['ranking', 'sector_economico', 'participacion_porcentual', 
                           'valor_aproximado_cop_billones', 'participacion_acumulada']]
    df_display.columns = ['Ranking', 'Sector Económico', 'Participación (%)', 
                         'Valor (COP)', 'Acumulado (%)']
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )

# 💡 SECCIÓN 4: INSIGHTS Y RECOMENDACIONES
st.markdown('<div class="section-header"><h2>💡 Insights Económicos</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="insights-card">
        <h4 style="color: {COLORS['primary']}; margin-top: 0;">🎯 Análisis de Fortalezas</h4>
        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
            <li><strong>Sector Minero-Energético:</strong> Base sólida con {sector_principal['participacion_porcentual']:.1f}% del PIB</li>
            <li><strong>Diversificación:</strong> {total_sectores} sectores activos en la economía</li>
            <li><strong>Servicios:</strong> Crecimiento en sectores terciarios</li>
            <li><strong>Agropecuario:</strong> Potencial en agricultura y ganadería</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="insights-card">
        <h4 style="color: {COLORS['secondary']}; margin-top: 0;">🚀 Oportunidades de Crecimiento</h4>
        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
            <li><strong>Diversificación:</strong> Reducir dependencia del sector extractivo</li>
            <li><strong>Valor Agregado:</strong> Procesar materias primas localmente</li>
            <li><strong>Turismo:</strong> Aprovechar recursos naturales y culturales</li>
            <li><strong>Tecnología:</strong> Desarrollar sectores de alta innovación</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Análisis de competitividad por sector
st.markdown("### 📈 Estrategias por Sector")

estrategias = {
    "Explotación de minas y canteras": {
        "color": "#d62728",
        "estrategia": "Diversificar hacia energías renovables y minería sostenible",
        "prioridad": "Alta"
    },
    "Agricultura ganadería caza silvicultura y pesca": {
        "color": "#2ca02c", 
        "estrategia": "Modernizar técnicas y desarrollar agroindustria",
        "prioridad": "Alta"
    },
    "Comercio al por mayor y al por menor": {
        "color": "#ff7f0e",
        "estrategia": "Digitalizar comercio y fortalecer cadenas de valor",
        "prioridad": "Media"
    }
}

for sector, info in estrategias.items():
    if sector in df_sectores['sector_economico'].values:
        sector_data = df_sectores[df_sectores['sector_economico'] == sector].iloc[0]
        
        st.markdown(f"""
        <div style="background: {info['color']}15; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {info['color']};">
            <div style="display: flex; justify-content: between; align-items: center;">
                <div style="flex-grow: 1;">
                    <strong style="color: {info['color']};">{sector}</strong><br>
                    <small>{info['estrategia']}</small>
                </div>
                <div style="text-align: right; margin-left: 1rem;">
                    <span style="background: {info['color']}; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">
                        {info['prioridad']}
                    </span><br>
                    <span style="font-weight: bold; color: {info['color']};">
                        {sector_data['participacion_porcentual']:.1f}%
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ✨ INSIGHTS Y PROPUESTAS DE ACCIÓN
st.markdown("---")
st.markdown("## ✨ **Insights y Propuestas de Acción**")

st.markdown(f"""
<div style="background: {COLORS['primary']}15; padding: 2rem; border-radius: 15px; border-left: 5px solid {COLORS['primary']}; margin: 2rem 0;">
    <h4 style="color: {COLORS['primary']}; margin-top: 0;">🎯 Análisis Estratégico del Perfil Económico</h4>
    
    <p><strong>Diagnóstico Principal:</strong></p>
    <p>El sector extractivo (minas y canteras) domina la economía departamental con más del 50% del PIB, lo que genera 
    una alta dependencia de recursos no renovables y volatilidad ante fluctuaciones internacionales de precios.</p>
    
    <p><strong>Propuestas de Acción:</strong></p>
    <ol>
        <li><strong>Diversificación Económica Urgente:</strong> Crear un fondo de diversificación que destine el 15% 
        de regalías mineras al desarrollo de sectores como agroindustria, turismo rural y servicios tecnológicos.</li>
        
        <li><strong>Fortalecimiento del Sector Agropecuario:</strong> Implementar programas de tecnificación agrícola 
        y ganadería sostenible para aumentar su participación del 8% actual al 15% en 5 años.</li>
        
        <li><strong>Desarrollo de Servicios de Alto Valor:</strong> Establecer un distrito de servicios empresariales 
        en Yopal que aproveche la conectividad y genere empleos calificados.</li>
        
        <li><strong>Encadenamientos Productivos:</strong> Promover la industrialización local de materias primas 
        para capturar mayor valor agregado en el territorio.</li>
    </ol>
    
    <p><strong>Meta 2030:</strong> Reducir la dependencia del sector extractivo del 50% al 35% del PIB, 
    mientras se duplica la participación de sectores de servicios y agroindustria.</p>
</div>
""", unsafe_allow_html=True)

# 🏛️ FOOTER
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, {COLORS['light']} 0%, white 100%); border-radius: 10px;">
    <p style="color: {COLORS['primary']}; font-size: 1.1rem; margin: 0;">
        📊 <strong>Perfil Económico de Casanare</strong>
    </p>
    <p style="color: #666; margin: 0.5rem 0; font-size: 0.9rem;">
        <em>Construyendo un futuro económico sostenible y diversificado</em>
    </p>
</div>
""", unsafe_allow_html=True)