"""
🛡️ Seguridad Ciudadana de Casanare
Análisis de indicadores de seguridad y convivencia ciudadana
"""

import streamlit as st
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.loader import load_seguridad
from utils.plotting import plot_barras_seguridad

# Configuración de la página
st.set_page_config(
    layout="wide", 
    page_title="🛡️ Seguridad Ciudadana - Casanare",
    page_icon="🛡️"
)

# 🎨 ESTILOS MODERNOS
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'warning': '#d62728',
    'danger': '#dc3545',
    'light': '#e6f3ff'
}

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-header {{
        background: linear-gradient(135deg, {COLORS['danger']} 0%, {COLORS['warning']} 100%);
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
    
    .metric-good {{
        border-left: 4px solid {COLORS['success']};
    }}
    
    .metric-warning {{
        border-left: 4px solid {COLORS['warning']};
    }}
    
    .metric-danger {{
        border-left: 4px solid {COLORS['danger']};
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
        background: linear-gradient(135deg, {COLORS['primary']}15 0%, {COLORS['secondary']}10 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid {COLORS['primary']};
        margin: 1rem 0;
    }}
    
    .alert-card {{
        background: linear-gradient(135deg, {COLORS['danger']}15 0%, {COLORS['warning']}10 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid {COLORS['danger']};
        margin: 1rem 0;
    }}
</style>
""", unsafe_allow_html=True)

# 🛡️ HEADER
st.markdown("""
<div class="main-header">
    <h1>🛡️ Seguridad Ciudadana de Casanare</h1>
    <h3>🚨 Indicadores de convivencia y seguridad territorial</h3>
</div>
""", unsafe_allow_html=True)

# 📊 CARGAR DATOS
@st.cache_data
def load_security_data():
    """Carga datos de seguridad"""
    return load_seguridad()

# Cargar datos
with st.spinner("🛡️ Cargando datos de seguridad..."):
    df_seguridad = load_security_data()

if df_seguridad.empty:
    st.error("❌ No se pudieron cargar los datos de seguridad.")
    st.stop()

# 🚨 SECCIÓN 1: KPIS DE SEGURIDAD
st.markdown('<div class="section-header"><h2>🚨 Indicadores Clave de Seguridad</h2></div>', unsafe_allow_html=True)

# Obtener datos específicos
homicidios = df_seguridad[df_seguridad['delito'] == 'Homicidios']['casos_2023'].iloc[0]
hurto_personas = df_seguridad[df_seguridad['delito'] == 'Hurto a personas']['casos_2023'].iloc[0]
violencia_intrafamiliar = df_seguridad[df_seguridad['delito'] == 'Violencia intrafamiliar']['casos_2023'].iloc[0]

# Calcular variaciones
var_homicidios = df_seguridad[df_seguridad['delito'] == 'Homicidios']['variacion_porcentual'].iloc[0]
var_hurto = df_seguridad[df_seguridad['delito'] == 'Hurto a personas']['variacion_porcentual'].iloc[0]
var_violencia = df_seguridad[df_seguridad['delito'] == 'Violencia intrafamiliar']['variacion_porcentual'].iloc[0]

col1, col2, col3 = st.columns(3)

with col1:
    # Determinar color según variación
    color_hom = COLORS['success'] if var_homicidios < 0 else COLORS['danger']
    delta_hom = f"{var_homicidios:+.1f}% vs 2022"
    
    st.metric(
        label="🔴 Homicidios (2023)",
        value=f"{homicidios:,}",
        delta=delta_hom,
        delta_color="inverse",
        help="Casos de homicidio reportados en 2023"
    )

with col2:
    color_hurto = COLORS['success'] if var_hurto < 0 else COLORS['danger']
    delta_hurto = f"{var_hurto:+.1f}% vs 2022"
    
    st.metric(
        label="👤 Hurto a Personas (2023)",
        value=f"{hurto_personas:,}",
        delta=delta_hurto,
        delta_color="inverse",
        help="Casos de hurto a personas reportados en 2023"
    )

with col3:
    color_vif = COLORS['success'] if var_violencia < 0 else COLORS['danger']
    delta_vif = f"{var_violencia:+.1f}% vs 2022"
    
    st.metric(
        label="🏠 Violencia Intrafamiliar (2023)",
        value=f"{violencia_intrafamiliar:,}",
        delta=delta_vif,
        delta_color="inverse",
        help="Casos de violencia intrafamiliar reportados en 2023"
    )

# 📊 SECCIÓN 2: ANÁLISIS GENERAL DE DELITOS
st.markdown('<div class="section-header"><h2>📊 Panorama General de Delitos</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2.5, 1])

with col1:
    # Gráfico principal de barras
    fig_seguridad = plot_barras_seguridad(df_seguridad)
    st.plotly_chart(fig_seguridad, use_container_width=True)

with col2:
    st.markdown("### 📈 Análisis de Tendencias")
    
    # Análisis por cada delito
    for _, delito in df_seguridad.iterrows():
        variacion = delito['variacion_porcentual']
        
        if variacion < -5:
            color = COLORS['success']
            tendencia = "Mejora significativa"
            icon = "📉"
        elif variacion < 0:
            color = COLORS['primary']
            tendencia = "Ligera mejora"
            icon = "📉"
        elif variacion < 5:
            color = COLORS['warning']
            tendencia = "Estable"
            icon = "➡️"
        else:
            color = COLORS['danger']
            tendencia = "Requiere atención"
            icon = "📈"
        
        st.markdown(f"""
        <div style="background: {color}15; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {color};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="color: {color};">{delito['delito']}</strong><br>
                    <small>{tendencia}</small>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 1.5rem;">{icon}</span><br>
                    <span style="font-weight: bold; color: {color};">
                        {variacion:+.1f}%
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 📋 SECCIÓN 3: ANÁLISIS DETALLADO
st.markdown('<div class="section-header"><h2>📋 Análisis Detallado por Tipo de Delito</h2></div>', unsafe_allow_html=True)

# Crear tabs para diferentes análisis
tab1, tab2, tab3 = st.tabs(["📊 Datos Generales", "🔍 Análisis Comparativo", "📈 Tendencias"])

with tab1:
    st.markdown("#### 📊 Estadísticas Generales de Seguridad")
    
    # Preparar datos para mostrar
    df_display = df_seguridad.copy()
    df_display['casos_2022'] = df_display['casos_2022'].map('{:,}'.format)
    df_display['casos_2023'] = df_display['casos_2023'].map('{:,}'.format)
    df_display['variacion_porcentual'] = df_display['variacion_porcentual'].map('{:+.1f}%'.format)
    
    # Renombrar columnas
    df_display.columns = ['Tipo de Delito', 'Casos 2022', 'Casos 2023', 'Variación (%)']
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )
    
    # Estadísticas adicionales
    total_delitos_2023 = df_seguridad['casos_2023'].sum()
    total_delitos_2022 = df_seguridad['casos_2022'].sum()
    variacion_total = ((total_delitos_2023 - total_delitos_2022) / total_delitos_2022) * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="highlight-number" style="color: {COLORS['primary']};">{total_delitos_2023:,}</p>
            <p class="highlight-label">Total Delitos 2023</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        color_var = COLORS['success'] if variacion_total < 0 else COLORS['danger']
        st.markdown(f"""
        <div class="metric-card">
            <p class="highlight-number" style="color: {color_var};">{variacion_total:+.1f}%</p>
            <p class="highlight-label">Variación Total 2022-2023</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        delito_mas_frecuente = df_seguridad.loc[df_seguridad['casos_2023'].idxmax(), 'delito']
        casos_mas_frecuente = df_seguridad['casos_2023'].max()
        st.markdown(f"""
        <div class="metric-card">
            <p class="highlight-number" style="color: {COLORS['warning']};">{casos_mas_frecuente:,}</p>
            <p class="highlight-label">Delito más frecuente:<br>{delito_mas_frecuente}</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("#### 🔍 Análisis Comparativo Nacional")
    
    st.markdown("""
    **📊 Contexto Nacional (Datos de referencia):**
    
    Los siguientes datos permiten contextualizar la situación de Casanare en el panorama nacional:
    """)
    
    # Análisis comparativo (datos simulados para demostración)
    analisis_comparativo = [
        {
            "delito": "Homicidios",
            "casanare": homicidios,
            "promedio_nacional": "15-25 por 100k hab",
            "evaluacion": "Dentro del promedio",
            "color": COLORS['warning']
        },
        {
            "delito": "Hurto a personas", 
            "casanare": hurto_personas,
            "promedio_nacional": "800-1500 casos",
            "evaluacion": "Dentro del rango esperado",
            "color": COLORS['primary']
        },
        {
            "delito": "Violencia intrafamiliar",
            "casanare": violencia_intrafamiliar,
            "promedio_nacional": "1000-2000 casos",
            "evaluacion": "Requiere monitoreo",
            "color": COLORS['warning']
        }
    ]
    
    for analisis in analisis_comparativo:
        st.markdown(f"""
        <div style="background: {analisis['color']}15; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {analisis['color']};">
            <div style="display: flex; justify-content: between; align-items: center;">
                <div style="flex-grow: 1;">
                    <strong style="color: {analisis['color']};">{analisis['delito']}</strong><br>
                    <small>Promedio nacional: {analisis['promedio_nacional']}</small><br>
                    <small>Casanare 2023: {analisis['casanare']:,} casos</small>
                </div>
                <div style="text-align: right; margin-left: 1rem;">
                    <span style="background: {analisis['color']}; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">
                        {analisis['evaluacion']}
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown("#### 📈 Análisis de Tendencias y Proyecciones")
    
    # Análisis de mejoras y deterioros
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📉 Delitos en Mejora")
        delitos_mejora = df_seguridad[df_seguridad['variacion_porcentual'] < 0]
        
        if not delitos_mejora.empty:
            for _, delito in delitos_mejora.iterrows():
                st.markdown(f"""
                <div style="background: {COLORS['success']}15; padding: 0.8rem; border-radius: 6px; margin: 0.3rem 0; border-left: 3px solid {COLORS['success']};">
                    <strong style="color: {COLORS['success']};">✅ {delito['delito']}</strong><br>
                    <small>Reducción: {delito['variacion_porcentual']:.1f}%</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No hay delitos con reducción en este período.")
    
    with col2:
        st.markdown("##### 📈 Delitos que Requieren Atención")
        delitos_aumento = df_seguridad[df_seguridad['variacion_porcentual'] > 0]
        
        if not delitos_aumento.empty:
            for _, delito in delitos_aumento.iterrows():
                st.markdown(f"""
                <div style="background: {COLORS['danger']}15; padding: 0.8rem; border-radius: 6px; margin: 0.3rem 0; border-left: 3px solid {COLORS['danger']};">
                    <strong style="color: {COLORS['danger']};">⚠️ {delito['delito']}</strong><br>
                    <small>Aumento: {delito['variacion_porcentual']:+.1f}%</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("Todos los delitos han mostrado reducción.")

# 💡 SECCIÓN 4: RECOMENDACIONES ESTRATÉGICAS
st.markdown('<div class="section-header"><h2>💡 Recomendaciones Estratégicas</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="insights-card">
        <h4 style="color: {COLORS['primary']}; margin-top: 0;">🎯 Estrategias de Prevención</h4>
        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
            <li><strong>Vigilancia Comunitaria:</strong> Fortalecer programas de seguridad ciudadana</li>
            <li><strong>Prevención Temprana:</strong> Programas educativos en instituciones</li>
            <li><strong>Iluminación y Espacios:</strong> Mejorar infraestructura urbana</li>
            <li><strong>Tecnología:</strong> Implementar sistemas de videovigilancia</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="alert-card">
        <h4 style="color: {COLORS['danger']}; margin-top: 0;">🚨 Atención Prioritaria</h4>
        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
            <li><strong>Violencia Intrafamiliar:</strong> Centros de atención y protección</li>
            <li><strong>Hurto a Personas:</strong> Patrullaje en zonas de alta incidencia</li>
            <li><strong>Articulación Institucional:</strong> Coordinación Policía-Fiscalía</li>
            <li><strong>Justicia Restaurativa:</strong> Programas de rehabilitación</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Metas específicas
st.markdown("### 🎯 Metas de Seguridad Ciudadana")

metas = [
    {
        "meta": "Reducir homicidios en 10%",
        "plazo": "2024",
        "estrategia": "Fortalecimiento del pie de fuerza y inteligencia",
        "color": COLORS['danger']
    },
    {
        "meta": "Disminuir hurto a personas en 15%",
        "plazo": "2024", 
        "estrategia": "Patrullaje preventivo y cámaras de seguridad",
        "color": COLORS['warning']
    },
    {
        "meta": "Reducir violencia intrafamiliar en 20%",
        "plazo": "2025",
        "estrategia": "Programas de prevención y atención integral",
        "color": COLORS['primary']
    }
]

for meta in metas:
    st.markdown(f"""
    <div style="background: {meta['color']}15; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {meta['color']};">
        <div style="display: flex; justify-content: between; align-items: center;">
            <div style="flex-grow: 1;">
                <strong style="color: {meta['color']};">{meta['meta']}</strong><br>
                <small>{meta['estrategia']}</small>
            </div>
            <div style="text-align: right; margin-left: 1rem;">
                <span style="background: {meta['color']}; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">
                    Meta {meta['plazo']}
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 🏛️ FOOTER
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, {COLORS['light']} 0%, white 100%); border-radius: 10px;">
    <p style="color: {COLORS['primary']}; font-size: 1.1rem; margin: 0;">
        🛡️ <strong>Seguridad Ciudadana de Casanare</strong>
    </p>
    <p style="color: #666; margin: 0.5rem 0; font-size: 0.9rem;">
        <em>Construyendo territorios seguros y en paz</em>
    </p>
</div>
""", unsafe_allow_html=True)
