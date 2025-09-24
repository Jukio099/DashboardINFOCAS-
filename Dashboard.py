"""
🏛️ Dashboard de Competitividad de Casanare
Panorama General del Departamento - Versión Modernizada
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.loader import (
    get_kpi_values, load_ciclo_vital, load_sector_economico, 
    load_empresarial, load_empresas_municipio
)

# Configuración de la página
st.set_page_config(
    layout="wide", 
    page_title="🏛️ Dashboard Casanare",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# 🎨 CSS GLOBAL: Alineación profesional de métricas
st.markdown("""
    <style>
        [data-testid="stMetric"] {
            text-align: left;
        }
        [data-testid="stMetric"] > div {
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

# 🎨 COLORES CORPORATIVOS DE CASANARE
COLORS = {
    'primary': '#1f77b4',      # Azul corporativo
    'secondary': '#ff7f0e',    # Naranja
    'success': '#2ca02c',      # Verde
    'warning': '#d62728',      # Rojo
    'info': '#9467bd',         # Púrpura
    'light': '#e6f3ff',        # Azul claro
    'gradient_start': '#1f77b4',
    'gradient_end': '#ff7f0e'
}

# 🎨 CSS MODERNO
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-header {{
        background: linear-gradient(135deg, {COLORS['gradient_start']} 0%, {COLORS['gradient_end']} 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        font-family: 'Inter', sans-serif;
    }}
    
    .main-header h1 {{
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }}
    
    .main-header h3 {{
        font-size: 1.2rem;
        font-weight: 400;
        opacity: 0.9;
        margin: 0;
    }}
    
    .metric-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #f0f0f0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }}
    
    .section-header {{
        background: linear-gradient(90deg, {COLORS['light']} 0%, white 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border-left: 4px solid {COLORS['primary']};
        margin: 2rem 0 1rem 0;
        font-family: 'Inter', sans-serif;
    }}
    
    .section-header h2 {{
        color: {COLORS['primary']};
        margin: 0;
        font-weight: 600;
    }}
    
    .stats-card {{
        background: linear-gradient(135deg, {COLORS['primary']}15 0%, {COLORS['secondary']}10 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid {COLORS['primary']}20;
        margin: 1rem 0;
    }}
    
    .highlight-number {{
        font-size: 2rem;
        font-weight: 700;
        color: {COLORS['primary']};
        margin: 0;
    }}
    
    .highlight-label {{
        font-size: 0.9rem;
        color: #666;
        margin: 0;
        font-weight: 500;
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{
        background-color: #f8f9fa;
    }}
    
    /* Métricas de Streamlit */
    [data-testid="metric-container"] {{
        background: white;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }}
</style>
""", unsafe_allow_html=True)

# 🏛️ HEADER PRINCIPAL
st.markdown("""
<div class="main-header">
    <h1>🏛️ Dashboard de Competitividad de Casanare</h1>
    <h3>📊 Transformando datos en decisiones inteligentes</h3>
</div>
""", unsafe_allow_html=True)

# 📊 CARGAR DATOS
@st.cache_data
def load_dashboard_data():
    """Carga todos los datos necesarios para el dashboard"""
    return {
        'kpis': get_kpi_values(),
        'ciclo_vital': load_ciclo_vital(),
        'sectores': load_sector_economico(),
        'empresas': load_empresarial(),
        'municipios': load_empresas_municipio()
    }

# Cargar datos
with st.spinner("🔄 Cargando datos del dashboard..."):
    data = load_dashboard_data()

# 🎯 SECCIÓN 1: KPIS PRINCIPALES CON MÉTRICAS MODERNAS
st.markdown('<div class="section-header"><h2>🎯 Indicadores Clave de Casanare</h2></div>', unsafe_allow_html=True)

kpis = data['kpis']

# Crear 4 columnas para las métricas principales con iconos GRANDES
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Icono grande con HTML personalizado
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <span style="font-size: 3rem;">👥</span>
    </div>
    """, unsafe_allow_html=True)
    st.metric(
        label="## 👥 Población (Proy. 2025)",
        value=f"{kpis.get('poblacion_2025', 0):,}",
        delta="En crecimiento",
        help="Proyección poblacional para 2025 según DANE"
    )

with col2:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <span style="font-size: 3rem;">💰</span>
    </div>
    """, unsafe_allow_html=True)
    pib_billones = kpis.get('pib_2023', 0) / 1000000  # Convertir a billones
    st.metric(
        label="## 💰 PIB Departamental (2023)",
        value=f"${pib_billones:.1f}B COP",
        delta="Crecimiento sostenido",
        help="Producto Interno Bruto departamental en billones de pesos"
    )

with col3:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <span style="font-size: 3rem;">🏆</span>
    </div>
    """, unsafe_allow_html=True)
    st.metric(
        label="## 🏆 Puntaje IDC (2025)",
        value=f"{kpis.get('puntaje_idc', 0):.2f}/10",
        delta=f"Ranking #{kpis.get('ranking_idc', 0)}",
        delta_color="inverse",
        help="Índice Departamental de Competitividad"
    )

with col4:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <span style="font-size: 3rem;">📈</span>
    </div>
    """, unsafe_allow_html=True)
    st.metric(
        label="## 📈 Ranking Nacional IDC",
        value=f"#{kpis.get('ranking_idc', 0)}",
        delta="De 32 departamentos",
        delta_color="off",
        help="Posición en el ranking nacional de competitividad"
    )

# 📊 SECCIÓN 2: VISUALIZACIONES PRINCIPALES
st.markdown('<div class="section-header"><h2>📊 Análisis Visual</h2></div>', unsafe_allow_html=True)

# Crear dos columnas para los gráficos principales
col1, col2 = st.columns([1.2, 0.8])

with col1:
    st.markdown("### 🍩 Composición Económica por Sectores")
    
    df_sectores = data['sectores']
    if not df_sectores.empty:
        # Treemap moderno con colores corporativos
        fig_treemap = px.treemap(
            df_sectores,
            path=['sector_economico'],
            values='participacion_porcentual',
            title="Participación de Sectores en el PIB (%)",
            color='participacion_porcentual',
            color_continuous_scale='YlGnBu',
            hover_data={
                'participacion_porcentual': ':.1f',
                'valor_aproximado_cop_billones': ':.1f'
            }
        )
        
        fig_treemap.update_layout(
            height=500,
            font=dict(size=12, family="Inter"),
            coloraxis_showscale=False
        )
        
        fig_treemap.update_traces(
            textinfo="label+percent entry",
            textfont_size=11,
            textfont_color="white",
            hovertemplate="<b>%{label}</b><br>" +
                         "Participación: %{value:.1f}%<br>" +
                         "<extra></extra>"
        )
        
        st.plotly_chart(fig_treemap, use_container_width=True)
        
        # Mostrar sector líder
        sector_lider = df_sectores.loc[df_sectores['participacion_porcentual'].idxmax()]
        st.markdown(f"""
        <div class="stats-card">
            <p class="highlight-number">{sector_lider['participacion_porcentual']:.1f}%</p>
            <p class="highlight-label">🥇 Sector Líder: {sector_lider['sector_economico']}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 👥 Estructura Demográfica")
    
    df_ciclo = data['ciclo_vital']
    if not df_ciclo.empty:
        # NUEVA PIRÁMIDE POBLACIONAL para mejor storytelling
        from utils.plotting import plot_piramide_poblacional
        fig_piramide = plot_piramide_poblacional(df_ciclo)
        st.plotly_chart(fig_piramide, use_container_width=True)
        
        # Estadísticas demográficas
        total_poblacion = df_ciclo['poblacion'].sum()
        st.markdown(f"""
        <div class="stats-card">
            <p class="highlight-number">{total_poblacion:,}</p>
            <p class="highlight-label">🏘️ Total Poblacional</p>
        </div>
        """, unsafe_allow_html=True)

# 🏢 SECCIÓN 3: ANÁLISIS EMPRESARIAL Y TERRITORIAL
st.markdown('<div class="section-header"><h2>🏢 Tejido Empresarial y Territorial</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏪 Empresas por Tamaño")
    
    df_empresas = data['empresas']
    if not df_empresas.empty:
        # Gráfico de barras moderno con gradiente
        fig_empresas = px.bar(
            df_empresas,
            x='tamaño_de_empresa',
            y='numero_de_empresas',
            title="Distribución del Tejido Empresarial",
            color='numero_de_empresas',
            color_continuous_scale=['#e3f2fd', '#1976d2', '#0d47a1'],
            text='numero_de_empresas'
        )
        
        fig_empresas.update_traces(
            texttemplate='%{text:,}',
            textposition='outside',
            textfont_size=12,
            textfont_color=COLORS['primary'],
            hovertemplate="<b>%{x}</b><br>" +
                         "Empresas: %{y:,}<br>" +
                         "<extra></extra>"
        )
        
        fig_empresas.update_layout(
            height=400,
            font=dict(family="Inter"),
            xaxis_title="Tamaño de Empresa",
            yaxis_title="Número de Empresas",
            showlegend=False,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig_empresas, use_container_width=True)
        
        # Total de empresas
        total_empresas = df_empresas['numero_de_empresas'].sum()
        st.markdown(f"""
        <div class="stats-card">
            <p class="highlight-number">{total_empresas:,}</p>
            <p class="highlight-label">📊 Total de Empresas Registradas</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🌆 Empresas por Municipio")
    
    df_municipios = data['municipios']
    if not df_municipios.empty:
        # Top 8 municipios con barras horizontales
        top_municipios = df_municipios.head(8)
        
        fig_municipios = px.bar(
            top_municipios,
            x='numero_de_empresas',
            y='municipio',
            orientation='h',
            title="Top Municipios Empresariales",
            color='numero_de_empresas',
            color_continuous_scale='Oranges',
            text='numero_de_empresas'
        )
        
        fig_municipios.update_traces(
            texttemplate='%{text:,}',
            textposition='outside',
            textfont_size=11,
            hovertemplate="<b>%{y}</b><br>" +
                         "Empresas: %{x:,}<br>" +
                         "<extra></extra>"
        )
        
        fig_municipios.update_layout(
            height=400,
            font=dict(family="Inter"),
            xaxis_title="Número de Empresas",
            yaxis_title="",
            showlegend=False
        )
        
        st.plotly_chart(fig_municipios, use_container_width=True)
        
        # Municipio líder
        municipio_lider = df_municipios.iloc[0]
        concentracion = (municipio_lider['numero_de_empresas'] / df_municipios['numero_de_empresas'].sum()) * 100
        st.markdown(f"""
        <div class="stats-card">
            <p class="highlight-number">{concentracion:.1f}%</p>
            <p class="highlight-label">🏆 Concentración en {municipio_lider['municipio']}</p>
        </div>
        """, unsafe_allow_html=True)

# 💡 SECCIÓN 4: INSIGHTS Y NAVEGACIÓN
st.markdown('<div class="section-header"><h2>💡 Insights Clave</h2></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="stats-card">
        <h4 style="color: #2ca02c; margin-top: 0;">🟢 Fortalezas</h4>
        <ul style="margin: 0; padding-left: 1rem;">
            <li>Economía sólida basada en recursos naturales</li>
            <li>Crecimiento poblacional sostenido</li>
            <li>Tejido empresarial diversificado</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stats-card">
        <h4 style="color: #ff7f0e; margin-top: 0;">🟡 Oportunidades</h4>
        <ul style="margin: 0; padding-left: 1rem;">
            <li>Diversificación económica</li>
            <li>Desarrollo del capital humano</li>
            <li>Fortalecimiento institucional</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stats-card">
        <h4 style="color: #1f77b4; margin-top: 0;">🔵 Navegación</h4>
        <p style="margin: 0.5rem 0;">Explora las secciones:</p>
        <ul style="margin: 0; padding-left: 1rem;">
            <li>📊 Perfil Económico</li>
            <li>🏢 Tejido Empresarial</li>
            <li>🛡️ Seguridad Ciudadana</li>
            <li>🩺 Salud Pública</li>
            <li>🎓 Educación</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ✨ SECCIÓN DE INSIGHTS Y PROPUESTAS
st.markdown('<div class="section-header"><h2>✨ Insights y Propuestas de Acción</h2></div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="background: {COLORS['primary']}15; padding: 2rem; border-radius: 15px; border-left: 5px solid {COLORS['primary']}; margin: 2rem 0;">
    <h4 style="color: {COLORS['primary']}; margin-top: 0;">🎯 Análisis Integral de Casanare</h4>
    
    <p><strong>Fortalezas Identificadas:</strong></p>
    <ul>
        <li><strong>Base económica sólida:</strong> El sector extractivo (minas y canteras) domina con {sector_lider['participacion_porcentual']:.1f}% del PIB, proporcionando estabilidad financiera departamental.</li>
        <li><strong>Tejido empresarial activo:</strong> {total_empresas:,} empresas registradas demuestran un ecosistema empresarial dinámico y diversificado.</li>
        <li><strong>Estructura poblacional favorable:</strong> Con {total_poblacion:,} habitantes, Casanare mantiene una distribución demográfica que favorece el crecimiento económico.</li>
    </ul>
    
    <p><strong>Oportunidades Estratégicas:</strong></p>
    <ul>
        <li><strong>Diversificación económica:</strong> Es crucial reducir la dependencia del sector extractivo invirtiendo en agricultura tecnificada, turismo sostenible y sectores de servicios.</li>
        <li><strong>Fortalecimiento empresarial:</strong> Implementar programas para que las {df_empresas[df_empresas['tamaño_de_empresa'] == 'Micro']['numero_de_empresas'].iloc[0]:,} microempresas puedan escalar a pequeñas y medianas empresas.</li>
        <li><strong>Desarrollo territorial equilibrado:</strong> Promover la descentralización empresarial desde {municipio_lider['municipio']} hacia otros municipios para un crecimiento más equitativo.</li>
    </ul>
    
    <p><strong>Acciones Prioritarias Recomendadas:</strong></p>
    <ol>
        <li>Crear un fondo de diversificación económica para sectores emergentes</li>
        <li>Establecer incubadoras de empresas en municipios con menor concentración empresarial</li>
        <li>Desarrollar un plan maestro de competitividad departamental a 10 años</li>
        <li>Fortalecer la articulación universidad-empresa-estado para la innovación</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# 💬 SECCIÓN DE COMENTARIOS
st.markdown('<div class="section-header"><h2>💬 Envíanos tus Comentarios</h2></div>', unsafe_allow_html=True)

st.markdown("""
<div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
    <p style="margin: 0; color: #666;">
        ¿Tienes sugerencias para mejorar este dashboard? ¿Te gustaría ver algún indicador adicional? 
        Tu retroalimentación es valiosa para seguir mejorando esta herramienta de análisis.
    </p>
</div>
""", unsafe_allow_html=True)

# Área de comentarios
comentario = st.text_area(
    "Tu comentario:",
    placeholder="Escribe aquí tus sugerencias, comentarios o preguntas sobre el dashboard...",
    height=100,
    help="Comparte tus ideas para mejorar el análisis de competitividad de Casanare"
)

col1, col2, col3 = st.columns([1, 1, 2])

with col2:
    if st.button("📤 Enviar comentario", type="primary", use_container_width=True):
        if comentario.strip():
            st.success("🎉 ¡Gracias por tu comentario! Lo tendremos en cuenta para futuras mejoras del dashboard.")
            st.balloons()
            
            # Mostrar el comentario (simulación)
            st.markdown(f"""
            <div style="background: #e8f5e8; padding: 1rem; border-radius: 8px; border-left: 4px solid #28a745; margin-top: 1rem;">
                <strong>💬 Tu comentario:</strong><br>
                <em>"{comentario}"</em>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Por favor, escribe un comentario antes de enviar.")

# 🏛️ FOOTER MODERNO
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, {COLORS['light']} 0%, white 100%); border-radius: 15px; margin-top: 2rem;">
    <h3 style="color: {COLORS['primary']}; margin-bottom: 0.5rem;">🏛️ Gobernación de Casanare</h3>
    <p style="color: #666; margin: 0.5rem 0;">📊 Dashboard de Competitividad Departamental</p>
    <p style="color: #999; margin: 0; font-size: 0.9rem;">
        💡 <em>Datos que impulsan el desarrollo territorial</em>
    </p>
</div>
""", unsafe_allow_html=True)