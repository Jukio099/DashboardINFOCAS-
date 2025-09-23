"""
🏛️ Dashboard de Competitividad de Casanare
Una herramienta visual para entender el desarrollo del departamento
"""

import streamlit as st
import sys
import os
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Configurar Streamlit para usar carpeta local (evita problemas de permisos)
os.environ['STREAMLIT_CONFIG_DIR'] = os.path.join(os.path.dirname(__file__), '.streamlit')

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.loader import load_all_data, get_kpi_values, get_ranking_data
from utils.plotting import plot_ranking_bars

# Configuración de la página
st.set_page_config(
    layout="wide", 
    page_title="🏛️ Dashboard Casanare",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# 🎨 COLORES DE CASANARE (Bandera)
COLORS_CASANARE = {
    'verde': '#228B22',      # Verde bandera
    'amarillo': '#FFD700',   # Amarillo bandera  
    'rojo': '#DC143C',       # Rojo bandera
    'verde_claro': '#90EE90',
    'amarillo_claro': '#FFFFE0',
    'rojo_claro': '#FFB6C1'
}

# 🎨 CSS para estilizar la aplicación
st.markdown(f"""
<style>
    .main-header {{
        background: linear-gradient(90deg, {COLORS_CASANARE['verde']} 0%, {COLORS_CASANARE['amarillo']} 50%, {COLORS_CASANARE['rojo']} 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    
    .metric-card {{
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid {COLORS_CASANARE['verde']};
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
    }}
    
    .section-header {{
        background: {COLORS_CASANARE['verde_claro']};
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border-left: 4px solid {COLORS_CASANARE['verde']};
        margin: 1rem 0;
    }}
    
    .highlight-box {{
        background: {COLORS_CASANARE['amarillo_claro']};
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid {COLORS_CASANARE['amarillo']};
        margin: 1rem 0;
    }}
    
    .success-metric {{
        color: {COLORS_CASANARE['verde']};
        font-weight: bold;
    }}
    
    .warning-metric {{
        color: {COLORS_CASANARE['amarillo']};
        font-weight: bold;
    }}
    
    .danger-metric {{
        color: {COLORS_CASANARE['rojo']};
        font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)

# 🏛️ HEADER PRINCIPAL
st.markdown("""
<div class="main-header">
    <h1>🏛️ Dashboard de Competitividad de Casanare</h1>
    <h3>📊 Datos que hablan por nuestro departamento</h3>
</div>
""", unsafe_allow_html=True)

# 📊 CARGAR TODOS LOS DATOS
@st.cache_data
def load_complete_data():
    """Carga todos los datos y los organiza por categorías"""
    data = load_all_data()
    df_main = data.get('general')
    
    if df_main is None or df_main.empty:
        return None
    
    # Organizar datos por pilares
    pilares = {}
    for pilar in df_main['Pilar_Competitividad'].unique():
        if pd.notna(pilar):
            pilares[pilar] = df_main[df_main['Pilar_Competitividad'] == pilar]
    
    return {
        'general': df_main,
        'pilares': pilares,
        'sectores': data.get('sector'),
        'empresas': data.get('empresarial'),
        'municipios': data.get('municipios')
    }

# Cargar datos
import pandas as pd
all_data = load_complete_data()

if all_data is None:
    st.error("❌ No se pudieron cargar los datos. Verifica que el archivo CSV esté disponible.")
    st.stop()

df_general = all_data['general']
pilares_data = all_data['pilares']

# 🎯 SECCIÓN 1: INDICADORES CLAVE
st.markdown('<div class="section-header"><h2>🎯 Casanare en Números</h2></div>', unsafe_allow_html=True)

if df_general is not None:
    kpis = get_kpi_values(df_general)
    
    # Crear columnas para métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### 👥 Población")
        st.metric(
            label="Habitantes (2025)",
            value=f"{kpis.get('poblacion', 0):,}",
            help="Total de personas que viven en Casanare"
        )
        st.markdown("🏘️ *Una comunidad en crecimiento*")
    
    with col2:
        st.markdown("### 💰 Economía")
        pib_value = kpis.get('pib_millones', 0)
        st.metric(
            label="PIB (COP Millones)",
            value=f"${pib_value:,.0f}",
            help="Producto Interno Bruto del departamento"
        )
        st.markdown("📈 *Motor económico regional*")
    
    with col3:
        st.markdown("### 🗺️ Territorio")
        st.metric(
            label="Superficie (km²)",
            value=f"{kpis.get('superficie', 0):,}",
            help="Extensión territorial de Casanare"
        )
        st.markdown("🌾 *Tierra de oportunidades*")
    
    with col4:
        st.markdown("### 🏆 Competitividad")
        idc_score = kpis.get('puntaje_idc', 0)
        st.metric(
            label="Puntaje IDC (sobre 10)",
            value=f"{idc_score:.2f}",
            help="Índice Departamental de Competitividad"
        )
        # Color según el puntaje
        if idc_score >= 7:
            st.markdown('<p class="success-metric">🟢 Muy competitivo</p>', unsafe_allow_html=True)
        elif idc_score >= 5:
            st.markdown('<p class="warning-metric">🟡 Moderadamente competitivo</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="danger-metric">🔴 Necesita mejorar</p>', unsafe_allow_html=True)

# 📊 SECCIÓN 2: ANÁLISIS POR PILARES DE COMPETITIVIDAD
st.markdown('<div class="section-header"><h2>🏗️ Pilares de Competitividad</h2></div>', unsafe_allow_html=True)
st.markdown("### 📋 ¿En qué somos buenos y dónde podemos mejorar?")

if pilares_data:
    # Crear pestañas para cada pilar
    pilar_names = list(pilares_data.keys())
    tabs = st.tabs([f"🔸 {pilar}" for pilar in pilar_names])
    
    for i, (pilar_name, tab) in enumerate(zip(pilar_names, tabs)):
        with tab:
            pilar_df = pilares_data[pilar_name]
            
            # Mostrar indicadores del pilar
            st.markdown(f"#### 📌 Indicadores de {pilar_name}")
            
            # Crear columnas para mostrar indicadores
            if len(pilar_df) > 0:
                cols = st.columns(min(3, len(pilar_df)))
                
                for idx, (_, row) in enumerate(pilar_df.iterrows()):
                    col_idx = idx % len(cols)
                    with cols[col_idx]:
                        # Mostrar cada indicador
                        st.markdown(f"**{row['Indicador']}**")
                        valor = row['Valor']
                        unidad = row['Unidad']
                        
                        # Formatear el valor según la unidad
                        if 'Puntaje' in str(unidad):
                            st.markdown(f"<h3 style='color: {COLORS_CASANARE['verde']};'>{valor:.2f}/10</h3>", unsafe_allow_html=True)
                            if valor >= 7:
                                st.markdown("🟢 Excelente")
                            elif valor >= 5:
                                st.markdown("🟡 Bueno")
                            else:
                                st.markdown("🔴 Mejorar")
                        elif '%' in str(unidad):
                            st.markdown(f"<h3 style='color: {COLORS_CASANARE['amarillo']};'>{valor}%</h3>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<h3 style='color: {COLORS_CASANARE['rojo']};'>{valor:,} {unidad}</h3>", unsafe_allow_html=True)
                        
                        # Mostrar ranking si existe
                        if pd.notna(row['Ranking_Nacional_2025']) and row['Ranking_Nacional_2025'] != 'N/A':
                            ranking = row['Ranking_Nacional_2025']
                            st.markdown(f"🏆 Posición nacional: **#{ranking}**")

# 🏢 SECCIÓN 3: ECONOMÍA Y EMPRESAS
st.markdown('<div class="section-header"><h2>🏢 Economía y Empresas</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏭 Sectores Económicos")
    df_sectores = all_data['sectores']
    if df_sectores is not None and not df_sectores.empty:
        # Gráfico de pastel con colores de Casanare
        fig_sectores = px.pie(
            df_sectores, 
            values='Participación Porcentual (%)', 
            names='Sector Económico',
            title="💼 ¿De dónde viene la riqueza de Casanare?",
            color_discrete_sequence=[COLORS_CASANARE['verde'], COLORS_CASANARE['amarillo'], 
                                   COLORS_CASANARE['rojo'], COLORS_CASANARE['verde_claro'],
                                   COLORS_CASANARE['amarillo_claro'], COLORS_CASANARE['rojo_claro']]
        )
        fig_sectores.update_layout(height=400)
        st.plotly_chart(fig_sectores, use_container_width=True)
        
        # Mostrar sector principal
        sector_principal = df_sectores.loc[df_sectores['Participación Porcentual (%)'].idxmax()]
        st.markdown(f"""
        <div class="highlight-box">
            <h4>🥇 Sector Principal</h4>
            <p><strong>{sector_principal['Sector Económico']}</strong></p>
            <p>Representa el <strong>{sector_principal['Participación Porcentual (%)']:.1f}%</strong> de la economía</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🏪 Empresas por Tamaño")
    df_empresas = all_data['empresas']
    if df_empresas is not None and not df_empresas.empty:
        # Gráfico de barras con colores de Casanare
        fig_empresas = px.bar(
            df_empresas,
            x='Tamaño de Empresa',
            y='Número de Empresas',
            title="🏪 ¿Qué tipo de empresas tenemos?",
            color='Número de Empresas',
            color_continuous_scale=[[0, COLORS_CASANARE['verde']], 
                                  [0.5, COLORS_CASANARE['amarillo']], 
                                  [1, COLORS_CASANARE['rojo']]]
        )
        fig_empresas.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_empresas, use_container_width=True)
        
        # Estadísticas de empresas
        total_empresas = df_empresas['Número de Empresas'].sum()
        st.markdown(f"""
        <div class="highlight-box">
            <h4>📊 Total de Empresas</h4>
            <p><strong>{total_empresas:,}</strong> empresas registradas</p>
            <p>Generando empleos y desarrollo</p>
        </div>
        """, unsafe_allow_html=True)

# 🌆 SECCIÓN 4: MUNICIPIOS
st.markdown('<div class="section-header"><h2>🌆 Nuestros Municipios</h2></div>', unsafe_allow_html=True)

df_municipios = all_data['municipios']
if df_municipios is not None and not df_municipios.empty:
    # Gráfico de barras horizontales para municipios
    fig_municipios = px.bar(
        df_municipios.head(8),  # Top 8 municipios
        x='Número de Empresas',
        y='Municipio',
        orientation='h',
        title="🏘️ Municipios con más empresas",
        color='Número de Empresas',
        color_continuous_scale=[[0, COLORS_CASANARE['verde']], 
                              [0.5, COLORS_CASANARE['amarillo']], 
                              [1, COLORS_CASANARE['rojo']]]
    )
    fig_municipios.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_municipios, use_container_width=True)
    
    # Top 3 municipios
    st.markdown("### 🏆 Top 3 Municipios")
    col1, col2, col3 = st.columns(3)
    
    top_municipios = df_municipios.head(3)
    colors = [COLORS_CASANARE['verde'], COLORS_CASANARE['amarillo'], COLORS_CASANARE['rojo']]
    medals = ['🥇', '🥈', '🥉']
    
    for i, (col, (_, row)) in enumerate(zip([col1, col2, col3], top_municipios.iterrows())):
        with col:
            st.markdown(f"""
            <div style="background: {colors[i]}20; padding: 1rem; border-radius: 10px; text-align: center;">
                <h3>{medals[i]} {row['Municipio']}</h3>
                <p><strong>{row['Número de Empresas']:,}</strong> empresas</p>
                <p>{row['Participación Porcentual (%)']:.1f}% del total</p>
            </div>
            """, unsafe_allow_html=True)

# 📈 SECCIÓN 5: RANKINGS NACIONALES
st.markdown('<div class="section-header"><h2>📈 ¿Cómo estamos a nivel nacional?</h2></div>', unsafe_allow_html=True)

df_ranking = get_ranking_data(df_general)
if not df_ranking.empty:
    # Crear gráfico de rankings con colores personalizados
    fig_ranking = go.Figure()
    
    # Añadir barras con colores según el puntaje
    for _, row in df_ranking.iterrows():
        valor = row['Valor']
        color = COLORS_CASANARE['verde'] if valor >= 7 else \
                COLORS_CASANARE['amarillo'] if valor >= 5 else \
                COLORS_CASANARE['rojo']
        
        fig_ranking.add_trace(go.Bar(
            x=[valor],
            y=[row['Indicador']],
            orientation='h',
            marker_color=color,
            name=row['Indicador'],
            showlegend=False,
            text=f"{valor:.2f}",
            textposition='outside'
        ))
    
    fig_ranking.update_layout(
        title="🏆 Rankings de Competitividad (Puntaje sobre 10)",
        xaxis_title="Puntaje",
        yaxis_title="",
        height=500,
        xaxis=dict(range=[0, 10])
    )
    
    st.plotly_chart(fig_ranking, use_container_width=True)
    
    # Resumen de rankings
    st.markdown("### 📊 Resumen de posiciones")
    bueno = len(df_ranking[df_ranking['Valor'] >= 7])
    regular = len(df_ranking[(df_ranking['Valor'] >= 5) & (df_ranking['Valor'] < 7)])
    mejorar = len(df_ranking[df_ranking['Valor'] < 5])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background: {COLORS_CASANARE['verde']}20; padding: 1rem; border-radius: 10px;">
            <h3 style="color: {COLORS_CASANARE['verde']};">🟢 Excelente</h3>
            <p><strong>{bueno}</strong> indicadores</p>
            <p>Puntaje ≥ 7.0</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: {COLORS_CASANARE['amarillo']}20; padding: 1rem; border-radius: 10px;">
            <h3 style="color: {COLORS_CASANARE['amarillo']};">🟡 Bueno</h3>
            <p><strong>{regular}</strong> indicadores</p>
            <p>Puntaje 5.0 - 6.9</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: {COLORS_CASANARE['rojo']}20; padding: 1rem; border-radius: 10px;">
            <h3 style="color: {COLORS_CASANARE['rojo']};">🔴 Mejorar</h3>
            <p><strong>{mejorar}</strong> indicadores</p>
            <p>Puntaje < 5.0</p>
        </div>
        """, unsafe_allow_html=True)

# 💡 SECCIÓN 6: CONCLUSIONES Y RECOMENDACIONES
st.markdown('<div class="section-header"><h2>💡 ¿Qué nos dicen estos datos?</h2></div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="highlight-box">
    <h3>🎯 Conclusiones principales:</h3>
    
    <h4>🟢 Fortalezas de Casanare:</h4>
    <ul>
        <li>💰 <strong>Economía sólida</strong>: PIB de ${kpis.get('pib_millones', 0):,.0f} millones</li>
        <li>👥 <strong>Población creciente</strong>: {kpis.get('poblacion', 0):,} habitantes</li>
        <li>🏢 <strong>Tejido empresarial activo</strong>: Miles de empresas generando empleo</li>
        <li>🌾 <strong>Territorio extenso</strong>: {kpis.get('superficie', 0):,} km² de oportunidades</li>
    </ul>
    
    <h4>🟡 Oportunidades de mejora:</h4>
    <ul>
        <li>📈 <strong>Competitividad</strong>: Trabajar en los indicadores con puntaje menor a 7</li>
        <li>🎓 <strong>Capital humano</strong>: Fortalecer educación y capacitación</li>
        <li>🏗️ <strong>Infraestructura</strong>: Mejorar conectividad y servicios</li>
        <li>🤝 <strong>Innovación</strong>: Promover empresas de mayor tamaño</li>
    </ul>
    
    <h4>🚀 El futuro de Casanare:</h4>
    <p>Con una base económica sólida y un territorio lleno de potencial, Casanare está bien posicionado para seguir creciendo. Los datos muestran que tenemos los fundamentos para ser un departamento líder en competitividad.</p>
</div>
""", unsafe_allow_html=True)

# 📱 FOOTER
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 2rem; background: {COLORS_CASANARE['verde']}10; border-radius: 10px;">
    <h3>🏛️ Gobernación de Casanare</h3>
    <p>📊 Dashboard desarrollado para la toma de decisiones basada en datos</p>
    <p>💚💛❤️ <em>Casanare, territorio de oportunidades</em></p>
</div>
""", unsafe_allow_html=True)