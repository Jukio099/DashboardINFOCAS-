"""
🩺 Salud Pública de Casanare
Análisis integral de indicadores de salud y bienestar poblacional
"""

import streamlit as st
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.loader import (
    load_morbilidad, load_calidad_agua, load_estructura_demografica,
    load_ciclo_vital, get_salud_kpis
)
from utils.plotting import (
    plot_area_evolucion, plot_area_calidad_agua, plot_dona_ciclo_vital
)

# Configuración de la página
st.set_page_config(
    layout="wide", 
    page_title="🩺 Salud Pública - Casanare",
    page_icon="🩺"
)

# 🎨 ESTILOS MODERNOS
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'warning': '#d62728',
    'health': '#6f42c1',
    'light': '#e6f3ff'
}

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-header {{
        background: linear-gradient(135deg, {COLORS['health']} 0%, {COLORS['primary']} 100%);
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
    
    .health-metric {{
        border-left: 4px solid {COLORS['health']};
    }}
    
    .highlight-number {{
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }}
    
    .highlight-label {{
        font-size: 1rem;
        color: #666;
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }}
    
    .insights-card {{
        background: linear-gradient(135deg, {COLORS['health']}15 0%, {COLORS['primary']}10 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid {COLORS['health']};
        margin: 1rem 0;
    }}
    
    .alert-health {{
        background: linear-gradient(135deg, {COLORS['warning']}15 0%, {COLORS['secondary']}10 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid {COLORS['warning']};
        margin: 1rem 0;
    }}
</style>
""", unsafe_allow_html=True)

# 🩺 HEADER
st.markdown("""
<div class="main-header">
    <h1>🩺 Salud Pública de Casanare</h1>
    <h3>⚕️ Indicadores de salud y bienestar poblacional</h3>
</div>
""", unsafe_allow_html=True)

# 📊 CARGAR DATOS
@st.cache_data
def load_health_data():
    """Carga todos los datos de salud"""
    return {
        'morbilidad': load_morbilidad(),
        'calidad_agua': load_calidad_agua(),
        'estructura_demo': load_estructura_demografica(),
        'ciclo_vital': load_ciclo_vital(),
        'kpis_salud': get_salud_kpis()
    }

# Cargar datos
with st.spinner("⚕️ Cargando datos de salud pública..."):
    data = load_health_data()

df_morbilidad = data['morbilidad']
df_agua = data['calidad_agua']
df_demo = data['estructura_demo']
df_ciclo = data['ciclo_vital']
kpis_salud = data['kpis_salud']

# ⚕️ SECCIÓN 1: KPIS DE SALUD
st.markdown('<div class="section-header"><h2>⚕️ Indicadores Clave de Salud</h2></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    # ICONO GRANDE para esperanza de vida
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <span style="font-size: 4rem;">💚</span>
    </div>
    """, unsafe_allow_html=True)
    
    esperanza_vida = kpis_salud.get('esperanza_vida', 76.2)
    st.metric(
        label="Esperanza de Vida al Nacer",
        value=f"{esperanza_vida:.1f} años",
        delta="Nivel nacional",
        help="Años promedio de vida esperados al nacer"
    )

with col2:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <span style="font-size: 4rem;">👶</span>
    </div>
    """, unsafe_allow_html=True)
    
    mortalidad_infantil = kpis_salud.get('mortalidad_infantil', 8.9)
    st.metric(
        label="Tasa de Mortalidad Infantil",
        value=f"{mortalidad_infantil:.1f}‰",
        delta="Por 1,000 nacidos vivos",
        delta_color="off",
        help="Muertes de menores de 1 año por cada 1,000 nacidos vivos"
    )

with col3:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <span style="font-size: 4rem;">🤱</span>
    </div>
    """, unsafe_allow_html=True)
    
    fecundidad_adolescente = kpis_salud.get('fecundidad_adolescente', 45.7)
    st.metric(
        label="Tasa de Fecundidad Adolescente",
        value=f"{fecundidad_adolescente:.1f}‰",
        delta="Por 1,000 mujeres 15-19",
        delta_color="off",
        help="Nacimientos por cada 1,000 mujeres de 15-19 años"
    )

# 📊 SECCIÓN 2: ANÁLISIS DE MORBILIDAD Y CALIDAD DEL AGUA
st.markdown('<div class="section-header"><h2>📊 Vigilancia Epidemiológica y Saneamiento</h2></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🦠 Morbilidad", "💧 Calidad del Agua"])

with tab1:
    st.markdown("### 🦠 Evolución de Casos de Dengue")
    
    if not df_morbilidad.empty:
        col1, col2 = st.columns([2.5, 1])
        
        with col1:
            # Gráfico de líneas para dengue
            # Gráfico de área - más impactante para mostrar tendencias de dengue
            fig_dengue = plot_area_evolucion(
                df_morbilidad, 
                'año', 
                'casos_de_dengue_reportados', 
                '🦟 Evolución de Casos de Dengue Reportados',
                'Casos de Dengue'
            )
            st.plotly_chart(fig_dengue, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 Estadísticas de Dengue")
            
            # Calcular estadísticas
            casos_2024 = df_morbilidad[df_morbilidad['año'] == 2024]['casos_dengue'].iloc[0]
            casos_2023 = df_morbilidad[df_morbilidad['año'] == 2023]['casos_dengue'].iloc[0]
            variacion_dengue = ((casos_2024 - casos_2023) / casos_2023) * 100
            promedio_casos = df_morbilidad['casos_dengue'].mean()
            max_casos = df_morbilidad['casos_dengue'].max()
            
            st.markdown(f"""
            <div class="metric-card health-metric">
                <p class="highlight-number" style="color: {COLORS['warning']};">{casos_2024:,}</p>
                <p class="highlight-label">Casos 2024</p>
            </div>
            """, unsafe_allow_html=True)
            
            color_var = COLORS['success'] if variacion_dengue < 0 else COLORS['warning']
            st.markdown(f"""
            <div class="metric-card">
                <p class="highlight-number" style="color: {color_var};">{variacion_dengue:+.1f}%</p>
                <p class="highlight-label">Variación 2023-2024</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <p class="highlight-number" style="color: {COLORS['primary']};">{promedio_casos:.0f}</p>
                <p class="highlight-label">Promedio Anual</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Análisis de otros vectores
        st.markdown("#### 🦟 Otras Enfermedades Vectoriales")
        
        col1, col2, col3 = st.columns(3)
        
        casos_2024_data = df_morbilidad[df_morbilidad['año'] == 2024].iloc[0]
        
        with col1:
            st.metric(
                label="🟡 Malaria",
                value=f"{casos_2024_data['casos_malaria']:,}",
                help="Casos de malaria reportados en 2024"
            )
        
        with col2:
            st.metric(
                label="🔵 Zika",
                value=f"{casos_2024_data['casos_zika']:,}",
                help="Casos de Zika reportados en 2024"
            )
        
        with col3:
            st.metric(
                label="🟣 Chikungunya",
                value=f"{casos_2024_data['casos_chikungunya']:,}",
                help="Casos de Chikungunya reportados en 2024"
            )
    
    else:
        st.warning("⚠️ No se encontraron datos de morbilidad.")

with tab2:
    st.markdown("### 💧 Índice de Riesgo de Calidad del Agua")
    
    if not df_agua.empty:
        col1, col2 = st.columns([2.5, 1])
        
        with col1:
            # Gráfico de área para calidad del agua
            fig_agua = plot_area_calidad_agua(df_agua)
            st.plotly_chart(fig_agua, use_container_width=True)
        
        with col2:
            st.markdown("#### 🎯 Análisis del Índice")
            
            # Últimos datos disponibles
            ultimo_indice = df_agua[df_agua['año'] == 2024]['indice_riesgo_calidad_agua'].iloc[0]
            municipios_sin_riesgo = df_agua[df_agua['año'] == 2024]['municipios_sin_riesgo'].iloc[0]
            municipios_riesgo_medio = df_agua[df_agua['año'] == 2024]['municipios_riesgo_medio'].iloc[0]
            
            # Clasificar riesgo
            if ultimo_indice <= 5:
                nivel_riesgo = "SIN RIESGO"
                color_riesgo = COLORS['success']
                descripcion = "Agua apta para consumo"
            elif ultimo_indice <= 14:
                nivel_riesgo = "RIESGO BAJO"
                color_riesgo = COLORS['primary']
                descripcion = "Agua de buena calidad"
            elif ultimo_indice <= 35:
                nivel_riesgo = "RIESGO MEDIO"
                color_riesgo = COLORS['warning']
                descripcion = "Requiere tratamiento"
            else:
                nivel_riesgo = "RIESGO ALTO"
                color_riesgo = COLORS['warning']
                descripcion = "Intervención urgente"
            
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: {color_riesgo};">
                <p class="highlight-number" style="color: {color_riesgo};">{ultimo_indice:.1f}</p>
                <p class="highlight-label">Índice 2024</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: {color_riesgo}15; padding: 1rem; border-radius: 8px; border-left: 4px solid {color_riesgo};">
                <strong style="color: {color_riesgo};">Nivel: {nivel_riesgo}</strong><br>
                <small>{descripcion}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Distribución por municipios
            st.markdown("#### 🏘️ Distribución Municipal")
            
            total_municipios = municipios_sin_riesgo + municipios_riesgo_medio
            pct_sin_riesgo = (municipios_sin_riesgo / total_municipios) * 100
            
            st.markdown(f"""
            - **Sin riesgo:** {municipios_sin_riesgo} municipios ({pct_sin_riesgo:.1f}%)
            - **Riesgo medio:** {municipios_riesgo_medio} municipios
            - **Riesgo alto:** 0 municipios
            """)
    
    else:
        st.warning("⚠️ No se encontraron datos de calidad del agua.")

# 👥 SECCIÓN 3: ESTRUCTURA DEMOGRÁFICA
st.markdown('<div class="section-header"><h2>👥 Estructura Demográfica y Ciclo Vital</h2></div>', unsafe_allow_html=True)

if not df_ciclo.empty:
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        # NUEVA PIRÁMIDE POBLACIONAL para mejor storytelling demográfico
        from utils.plotting import plot_piramide_poblacional
        fig_piramide = plot_piramide_poblacional(df_ciclo)
        st.plotly_chart(fig_piramide, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Análisis por Grupos Etarios")
        
        # Análisis de la estructura poblacional
        total_poblacion = df_ciclo['poblacion'].sum()
        
        for _, grupo in df_ciclo.iterrows():
            porcentaje = (grupo['poblacion'] / total_poblacion) * 100
            
            # Determinar color según grupo etario
            if 'infancia' in grupo['ciclo_vital'].lower() or 'adolescencia' in grupo['ciclo_vital'].lower():
                color = COLORS['primary']
            elif 'juventud' in grupo['ciclo_vital'].lower() or 'adultez' in grupo['ciclo_vital'].lower():
                color = COLORS['success']
            else:
                color = COLORS['health']
            
            st.markdown(f"""
            <div style="background: {color}15; padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: {color};">{grupo['ciclo_vital']}</strong><br>
                        <small>{grupo['poblacion']:,} personas</small>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 1.2rem; font-weight: bold; color: {color};">
                            {porcentaje:.1f}%
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Indicadores demográficos clave
        st.markdown("### 📈 Indicadores Demográficos")
        
        # Dependencia demográfica
        menores_15 = df_ciclo[df_ciclo['ciclo_vital'].str.contains('infancia|Primera infancia', case=False, na=False)]['poblacion'].sum()
        mayores_60 = df_ciclo[df_ciclo['ciclo_vital'].str.contains('mayor', case=False, na=False)]['poblacion'].sum()
        poblacion_activa = total_poblacion - menores_15 - mayores_60
        
        if poblacion_activa > 0:
            razon_dependencia = ((menores_15 + mayores_60) / poblacion_activa) * 100
            
            st.markdown(f"""
            <div class="metric-card">
                <p class="highlight-number" style="color: {COLORS['health']};">{razon_dependencia:.1f}</p>
                <p class="highlight-label">Razón de Dependencia</p>
            </div>
            """, unsafe_allow_html=True)

else:
    st.warning("⚠️ No se encontraron datos de estructura demográfica.")

# 💡 SECCIÓN 4: ANÁLISIS Y RECOMENDACIONES
st.markdown('<div class="section-header"><h2>💡 Análisis y Recomendaciones en Salud</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="insights-card">
        <h4 style="color: {COLORS['health']}; margin-top: 0;">🎯 Logros en Salud Pública</h4>
        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
            <li><strong>Esperanza de vida:</strong> {esperanza_vida:.1f} años (nivel nacional)</li>
            <li><strong>Mortalidad infantil:</strong> {mortalidad_infantil:.1f}‰ (cumple meta ODS)</li>
            <li><strong>Calidad del agua:</strong> Mayoría de municipios sin riesgo</li>
            <li><strong>Vigilancia epidemiológica:</strong> Sistema de monitoreo activo</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="alert-health">
        <h4 style="color: {COLORS['warning']}; margin-top: 0;">🚨 Áreas de Mejora</h4>
        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
            <li><strong>Enfermedades vectoriales:</strong> Control del dengue y vectores</li>
            <li><strong>Fecundidad adolescente:</strong> Programas de educación sexual</li>
            <li><strong>Saneamiento básico:</strong> Mejorar acceso en zonas rurales</li>
            <li><strong>Atención primaria:</strong> Fortalecer la red de servicios</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Estrategias específicas por área
st.markdown("### 📋 Estrategias Prioritarias")

estrategias = [
    {
        "area": "🦟 Control de Vectores",
        "objetivo": "Reducir casos de dengue en 30%",
        "acciones": "Eliminación de criaderos, fumigación, educación comunitaria",
        "color": COLORS['warning']
    },
    {
        "area": "💧 Agua y Saneamiento",
        "objetivo": "100% municipios sin riesgo alto",
        "acciones": "Mejoramiento de plantas de tratamiento, vigilancia de calidad",
        "color": COLORS['primary']
    },
    {
        "area": "👶 Salud Materno-Infantil",
        "objetivo": "Reducir mortalidad infantil a <8‰",
        "acciones": "Atención prenatal, parto humanizado, control de crecimiento",
        "color": COLORS['success']
    }
]

for estrategia in estrategias:
    st.markdown(f"""
    <div style="background: {estrategia['color']}15; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {estrategia['color']};">
        <div style="display: flex; justify-content: between; align-items: center;">
            <div style="flex-grow: 1;">
                <strong style="color: {estrategia['color']};">{estrategia['area']}</strong><br>
                <small><strong>Objetivo:</strong> {estrategia['objetivo']}</small><br>
                <small><strong>Acciones:</strong> {estrategia['acciones']}</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ✨ SECCIÓN DE INSIGHTS Y PROPUESTAS
st.markdown('<div class="section-header"><h2>✨ Insights y Propuestas de Acción</h2></div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="background: {COLORS['health']}15; padding: 2rem; border-radius: 15px; border-left: 5px solid {COLORS['health']}; margin: 2rem 0;">
    <h4 style="color: {COLORS['health']}; margin-top: 0;">🎯 Análisis Integral de Salud Pública</h4>
    
    <p><strong>Logros Destacados:</strong></p>
    <ul>
        <li><strong>Esperanza de vida competitiva:</strong> Con {esperanza_vida:.1f} años, Casanare se mantiene al nivel del promedio nacional, reflejando condiciones de vida favorables.</li>
        <li><strong>Control de mortalidad infantil:</strong> La tasa de {mortalidad_infantil:.1f}‰ cumple con los estándares de los Objetivos de Desarrollo Sostenible (meta <10‰).</li>
        <li><strong>Calidad del agua aceptable:</strong> El índice de riesgo actual permite un suministro relativamente seguro en la mayoría de municipios.</li>
    </ul>
    
    <p><strong>Desafíos a Priorizar:</strong></p>
    <ul>
        <li><strong>Enfermedades vectoriales:</strong> Los casos de dengue requieren un sistema de vigilancia epidemiológica más robusto y estrategias de control vectorial sostenibles.</li>
        <li><strong>Fecundidad adolescente:</strong> La tasa de {fecundidad_adolescente:.1f}‰ indica la necesidad de fortalecer programas de educación sexual integral y salud reproductiva.</li>
        <li><strong>Equidad territorial:</strong> Garantizar que todos los municipios mantengan estándares similares de calidad del agua y acceso a servicios de salud.</li>
    </ul>
    
    <p><strong>Acciones Estratégicas Recomendadas:</strong></p>
    <ol>
        <li><strong>Implementar un sistema de alerta temprana</strong> para enfermedades transmitidas por vectores con foco en dengue y malaria</li>
        <li><strong>Desarrollar centros de salud amigables para jóvenes</strong> que ofrezcan servicios de salud sexual y reproductiva</li>
        <li><strong>Crear un programa de mejoramiento continuo</strong> de la calidad del agua potable en municipios rurales</li>
        <li><strong>Fortalecer la atención primaria en salud</strong> con énfasis en medicina preventiva y promoción de la salud</li>
        <li><strong>Establecer indicadores de seguimiento</strong> a la mortalidad materna extrema para intervenciones oportunas</li>
    </ol>
    
    <p><strong>Meta Departamental 2025-2030:</strong></p>
    <p style="font-style: italic; background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid {COLORS['success']};">
        "Posicionar a Casanare como un departamento modelo en salud pública rural, con indicadores de salud materna e infantil 
        por encima del promedio nacional y un sistema de vigilancia epidemiológica ejemplar para la región de la Orinoquía."
    </p>
</div>
""", unsafe_allow_html=True)

# 🏛️ FOOTER
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, {COLORS['light']} 0%, white 100%); border-radius: 10px;">
    <p style="color: {COLORS['health']}; font-size: 1.1rem; margin: 0;">
        🩺 <strong>Salud Pública de Casanare</strong>
    </p>
    <p style="color: #666; margin: 0.5rem 0; font-size: 0.9rem;">
        <em>Promoviendo la salud y el bienestar de todos los casanareños</em>
    </p>
</div>
""", unsafe_allow_html=True)
