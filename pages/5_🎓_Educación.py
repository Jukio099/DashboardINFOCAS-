"""
🎓 Educación y Capital Humano de Casanare
Análisis integral del sistema educativo y formación profesional
"""

import streamlit as st
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.loader import (
    load_graduados, load_desercion, get_educacion_kpis
)
from utils.plotting import (
    plot_bar_graduados, plot_barras_desercion_municipios
)

# Configuración de la página
st.set_page_config(
    layout="wide", 
    page_title="🎓 Educación - Casanare",
    page_icon="🎓"
)

# 🎨 ESTILOS MODERNOS
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'warning': '#d62728',
    'education': '#17a2b8',
    'light': '#e6f3ff'
}

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-header {{
        background: linear-gradient(135deg, {COLORS['education']} 0%, {COLORS['primary']} 100%);
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
    
    .education-metric {{
        border-left: 4px solid {COLORS['education']};
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
        background: linear-gradient(135deg, {COLORS['education']}15 0%, {COLORS['primary']}10 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid {COLORS['education']};
        margin: 1rem 0;
    }}
    
    .area-card {{
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        border-left: 4px solid {COLORS['secondary']};
    }}
    
    .municipio-desercion {{
        background: white;
        padding: 0.8rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 0.3rem 0;
    }}
</style>
""", unsafe_allow_html=True)

# 🎓 HEADER
st.markdown("""
<div class="main-header">
    <h1>🎓 Educación y Capital Humano de Casanare</h1>
    <h3>📚 Formación, conocimiento y desarrollo del talento regional</h3>
</div>
""", unsafe_allow_html=True)

# 📊 CARGAR DATOS
@st.cache_data
def load_education_data():
    """Carga todos los datos de educación"""
    return {
        'graduados': load_graduados(),
        'desercion': load_desercion(),
        'kpis_educacion': get_educacion_kpis()
    }

# Cargar datos
with st.spinner("🎓 Cargando datos de educación..."):
    data = load_education_data()

df_graduados = data['graduados']
df_desercion = data['desercion']
kpis_educacion = data['kpis_educacion']

# 📚 SECCIÓN 1: KPIS DE EDUCACIÓN
st.markdown('<div class="section-header"><h2>📚 Indicadores Clave de Educación</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    tasa_desercion = kpis_educacion.get('tasa_desercion_promedio', 0)
    # Meta nacional: <3% deserción
    color_desercion = COLORS['success'] if tasa_desercion < 3 else COLORS['warning'] if tasa_desercion < 5 else COLORS['warning']
    
    st.metric(
        label="📉 Tasa de Deserción Promedio",
        value=f"{tasa_desercion:.1f}%",
        delta="Sector oficial",
        delta_color="inverse",
        help="Promedio de deserción escolar en el sector oficial"
    )

with col2:
    total_graduados = kpis_educacion.get('total_graduados', 0)
    
    st.metric(
        label="🎓 Total de Graduados",
        value=f"{total_graduados:,}",
        delta="Educación superior",
        help="Total de graduados de educación superior por área de conocimiento"
    )

# Métricas adicionales (calculadas)
if not df_desercion.empty and not df_graduados.empty:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Municipio con menor deserción
        mejor_municipio = df_desercion.loc[df_desercion['tasa_desercion'].idxmin()]
        st.metric(
            label="🏆 Mejor Municipio",
            value=f"{mejor_municipio['tasa_desercion']:.1f}%",
            delta=mejor_municipio['municipio'],
            help="Municipio con menor tasa de deserción"
        )
    
    with col2:
        # Área con más graduados
        area_lider = df_graduados.loc[df_graduados['numero_de_graduados'].idxmax()]
        st.metric(
            label="🥇 Área Líder",
            value=f"{area_lider['numero_de_graduados']:,}",
            delta=area_lider['area_de_conocimiento'][:20] + "...",
            help="Área de conocimiento con más graduados"
        )
    
    with col3:
        # Diversificación académica
        total_areas = len(df_graduados)
        st.metric(
            label="📊 Áreas de Conocimiento",
            value=total_areas,
            delta="Diversificación académica",
            help="Número de áreas de conocimiento con graduados"
        )

# 🎓 SECCIÓN 2: GRADUADOS POR ÁREA DE CONOCIMIENTO
st.markdown('<div class="section-header"><h2>🎓 Formación Profesional por Área</h2></div>', unsafe_allow_html=True)

if not df_graduados.empty:
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        # Gráfico de dona para graduados
        # Gráfico de barras horizontales - más legible que dona para muchas categorías
        fig_graduados = plot_bar_graduados(df_graduados)
        st.plotly_chart(fig_graduados, use_container_width=True)
    
    with col2:
        st.markdown("### 🏆 Top 5 Áreas de Conocimiento")
        
        top5_areas = df_graduados.nlargest(5, 'numero_de_graduados')
        total_graduados_areas = df_graduados['numero_de_graduados'].sum()
        
        for i, (_, area) in enumerate(top5_areas.iterrows(), 1):
            participacion = (area['numero_de_graduados'] / total_graduados_areas) * 100
            
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
                color = COLORS['education']
            
            # Truncar nombre si es muy largo
            area_name = area['area_de_conocimiento']
            if len(area_name) > 35:
                area_name = area_name[:32] + "..."
            
            st.markdown(f"""
            <div class="area-card" style="border-left-color: {color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{medal} {area_name}</strong><br>
                        <small style="color: #666;">{participacion:.1f}% del total</small>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 1.2rem; font-weight: bold; color: {COLORS['education']};">
                            {area['numero_de_graduados']:,}
                        </span><br>
                        <small style="color: #666;">graduados</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Análisis de diversificación
        st.markdown("### 📊 Análisis de Diversificación")
        
        # Concentración de las top 3 áreas
        top3_concentracion = top5_areas.head(3)['numero_de_graduados'].sum()
        concentracion_pct = (top3_concentracion / total_graduados_areas) * 100
        
        if concentracion_pct > 70:
            nivel_concentracion = "Alta"
            color_conc = COLORS['warning']
        elif concentracion_pct > 50:
            nivel_concentracion = "Moderada"
            color_conc = COLORS['secondary']
        else:
            nivel_concentracion = "Baja"
            color_conc = COLORS['success']
        
        st.markdown(f"""
        <div class="metric-card">
            <p class="highlight-number" style="color: {color_conc};">{concentracion_pct:.1f}%</p>
            <p class="highlight-label">Concentración Top 3 - {nivel_concentracion}</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.warning("⚠️ No se encontraron datos de graduados.")

# 📉 SECCIÓN 3: DESERCIÓN ESCOLAR POR MUNICIPIO
st.markdown('<div class="section-header"><h2>📉 Deserción Escolar por Municipio</h2></div>', unsafe_allow_html=True)

if not df_desercion.empty:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfico de barras horizontales para deserción
        fig_desercion = plot_barras_desercion_municipios(df_desercion)
        st.plotly_chart(fig_desercion, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Análisis de Deserción")
        
        # Estadísticas de deserción
        tasa_max = df_desercion['tasa_desercion'].max()
        tasa_min = df_desercion['tasa_desercion'].min()
        tasa_promedio = df_desercion['tasa_desercion'].mean()
        municipio_max = df_desercion.loc[df_desercion['tasa_desercion'].idxmax(), 'municipio']
        municipio_min = df_desercion.loc[df_desercion['tasa_desercion'].idxmin(), 'municipio']
        
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: {COLORS['success']};">
            <p class="highlight-number" style="color: {COLORS['success']};">{tasa_min:.1f}%</p>
            <p class="highlight-label">Menor Deserción<br>{municipio_min}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: {COLORS['warning']};">
            <p class="highlight-number" style="color: {COLORS['warning']};">{tasa_max:.1f}%</p>
            <p class="highlight-label">Mayor Deserción<br>{municipio_max}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: {COLORS['education']};">
            <p class="highlight-number" style="color: {COLORS['education']};">{tasa_promedio:.1f}%</p>
            <p class="highlight-label">Promedio Departamental</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Clasificación de municipios
        st.markdown("### 🏘️ Clasificación Municipal")
        
        municipios_buenos = len(df_desercion[df_desercion['tasa_desercion'] < 4])
        municipios_regulares = len(df_desercion[(df_desercion['tasa_desercion'] >= 4) & (df_desercion['tasa_desercion'] < 7)])
        municipios_criticos = len(df_desercion[df_desercion['tasa_desercion'] >= 7])
        
        st.markdown(f"""
        - **🟢 Excelente (<4%):** {municipios_buenos} municipios
        - **🟡 Regular (4-7%):** {municipios_regulares} municipios  
        - **🔴 Crítico (>7%):** {municipios_criticos} municipios
        """)

else:
    st.warning("⚠️ No se encontraron datos de deserción.")

# 📊 SECCIÓN 4: ANÁLISIS DETALLADO
st.markdown('<div class="section-header"><h2>📊 Análisis Detallado del Sistema Educativo</h2></div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📈 Graduados", "📉 Deserción", "💡 Comparativo"])

with tab1:
    st.markdown("#### 🎓 Análisis Detallado de Graduados")
    
    if not df_graduados.empty:
        # Preparar datos para mostrar
        df_grad_display = df_graduados.copy()
        df_grad_display['participacion_pct'] = (df_grad_display['numero_de_graduados'] / df_grad_display['numero_de_graduados'].sum() * 100).round(1)
        df_grad_display['acumulado_pct'] = df_grad_display['participacion_pct'].cumsum()
        df_grad_display['ranking'] = range(1, len(df_grad_display) + 1)
        
        # Formatear para visualización
        df_grad_display['numero_de_graduados'] = df_grad_display['numero_de_graduados'].map('{:,}'.format)
        df_grad_display['participacion_pct'] = df_grad_display['participacion_pct'].map('{:.1f}%'.format)
        df_grad_display['acumulado_pct'] = df_grad_display['acumulado_pct'].map('{:.1f}%'.format)
        
        # Mostrar tabla
        df_display = df_grad_display[['ranking', 'area_de_conocimiento', 'numero_de_graduados', 'participacion_pct', 'acumulado_pct']]
        df_display.columns = ['Ranking', 'Área de Conocimiento', 'N° Graduados', 'Participación (%)', 'Acumulado (%)']
        
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )
        
        # Análisis de tendencias académicas
        st.markdown("#### 📊 Tendencias Académicas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **🔍 Análisis de Concentración:**
            - **Top 3 áreas:** {concentracion_pct:.1f}% de graduados
            - **Diversificación:** {len(df_graduados)} áreas activas
            - **Área líder:** {area_lider['area_de_conocimiento']} ({area_lider['numero_de_graduados']:,} graduados)
            """)
        
        with col2:
            st.markdown(f"""
            **📈 Oportunidades de Crecimiento:**
            - Fortalecer áreas STEM
            - Diversificar oferta académica
            - Articular con sector productivo
            """)

with tab2:
    st.markdown("#### 📉 Análisis Detallado de Deserción")
    
    if not df_desercion.empty:
        # Preparar datos de deserción
        df_des_display = df_desercion.copy()
        df_des_display['clasificacion'] = df_des_display['tasa_desercion'].apply(
            lambda x: 'Excelente' if x < 4 else 'Regular' if x < 7 else 'Crítico'
        )
        df_des_display['ranking'] = df_des_display['tasa_desercion'].rank(method='min').astype(int)
        
        # Formatear para visualización
        df_des_display['tasa_desercion'] = df_des_display['tasa_desercion'].map('{:.1f}%'.format)
        
        # Mostrar tabla ordenada por mejor desempeño
        df_des_display = df_des_display.sort_values('ranking')
        df_display = df_des_display[['ranking', 'municipio', 'tasa_desercion', 'clasificacion']]
        df_display.columns = ['Ranking', 'Municipio', 'Tasa Deserción (%)', 'Clasificación']
        
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )
        
        # Análisis por clasificación
        st.markdown("#### 🎯 Estrategias por Clasificación")
        
        estrategias_desercion = [
            {
                "clasificacion": "Excelente (<4%)",
                "estrategia": "Mantener buenas prácticas y ser ejemplo para otros municipios",
                "color": COLORS['success']
            },
            {
                "clasificacion": "Regular (4-7%)",
                "estrategia": "Implementar programas de retención y apoyo pedagógico",
                "color": COLORS['secondary']
            },
            {
                "clasificacion": "Crítico (>7%)",
                "estrategia": "Intervención urgente con programas integrales",
                "color": COLORS['warning']
            }
        ]
        
        for estrategia in estrategias_desercion:
            st.markdown(f"""
            <div style="background: {estrategia['color']}15; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {estrategia['color']};">
                <strong style="color: {estrategia['color']};">{estrategia['clasificacion']}</strong><br>
                <small>{estrategia['estrategia']}</small>
            </div>
            """, unsafe_allow_html=True)

with tab3:
    st.markdown("#### 💡 Análisis Comparativo Regional")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **📊 Contexto Nacional (Referencias):**
        
        **Deserción Escolar:**
        - **Meta nacional:** <3% deserción sector oficial
        - **Promedio nacional:** ~4-5% deserción
        - **Casanare:** {tasa_desercion:.1f}% promedio
        - **Evaluación:** {"✅ Por debajo" if tasa_desercion < 4 else "⚠️ Dentro" if tasa_desercion < 6 else "🔴 Por encima"} del promedio
        """)
    
    with col2:
        st.markdown(f"""
        **🎓 Educación Superior:**
        - **Total graduados:** {total_graduados:,}
        - **Áreas diversificadas:** {len(df_graduados) if not df_graduados.empty else 0}
        - **Concentración académica:** {concentracion_pct:.1f}% en top 3
        - **Oportunidad:** {"Alta" if concentracion_pct > 60 else "Media"} diversificación
        """)

# 💡 SECCIÓN 5: RECOMENDACIONES ESTRATÉGICAS
st.markdown('<div class="section-header"><h2>💡 Recomendaciones para el Sistema Educativo</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="insights-card">
        <h4 style="color: {COLORS['education']}; margin-top: 0;">🎯 Fortalezas del Sistema</h4>
        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
            <li><strong>Formación técnica:</strong> Graduados en ingeniería y áreas técnicas</li>
            <li><strong>Educación pedagógica:</strong> Fuerte formación en ciencias de la educación</li>
            <li><strong>Municipios exitosos:</strong> {municipios_buenos} municipios con baja deserción</li>
            <li><strong>Diversificación:</strong> {len(df_graduados) if not df_graduados.empty else 0} áreas de conocimiento activas</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="insights-card">
        <h4 style="color: {COLORS['warning']}; margin-top: 0;">🚀 Áreas de Mejora</h4>
        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
            <li><strong>Deserción crítica:</strong> {municipios_criticos} municipios requieren intervención</li>
            <li><strong>Equidad territorial:</strong> Reducir brechas entre municipios</li>
            <li><strong>Diversificación:</strong> Promover nuevas áreas STEM</li>
            <li><strong>Articulación:</strong> Conectar formación con mercado laboral</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Estrategias específicas por componente
st.markdown("### 📋 Plan de Acción Educativo")

planes = [
    {
        "componente": "🎓 Educación Superior",
        "objetivo": "Diversificar oferta académica en 25%",
        "acciones": "Nuevos programas STEM, articulación universidad-empresa, becas especializadas",
        "color": COLORS['education']
    },
    {
        "componente": "📉 Retención Escolar",
        "objetivo": "Reducir deserción promedio a <4%",
        "acciones": "Programas de apoyo pedagógico, alimentación escolar, transporte rural",
        "color": COLORS['warning']
    },
    {
        "componente": "🌐 Calidad Educativa",
        "objetivo": "Mejorar resultados en pruebas nacionales",
        "acciones": "Capacitación docente, infraestructura educativa, tecnología en aulas",
        "color": COLORS['success']
    }
]

for plan in planes:
    st.markdown(f"""
    <div style="background: {plan['color']}15; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {plan['color']};">
        <div>
            <strong style="color: {plan['color']};">{plan['componente']}</strong><br>
            <small><strong>Objetivo:</strong> {plan['objetivo']}</small><br>
            <small><strong>Acciones:</strong> {plan['acciones']}</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 🏛️ FOOTER
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, {COLORS['light']} 0%, white 100%); border-radius: 10px;">
    <p style="color: {COLORS['education']}; font-size: 1.1rem; margin: 0;">
        🎓 <strong>Educación y Capital Humano de Casanare</strong>
    </p>
    <p style="color: #666; margin: 0.5rem 0; font-size: 0.9rem;">
        <em>Formando el talento que transformará nuestro territorio</em>
    </p>
</div>
""", unsafe_allow_html=True)
