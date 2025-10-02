"""
Módulo simplificado para la carga de datos limpios desde CSV.
Lee EXCLUSIVAMENTE desde la carpeta data/clean/ - SIN lógica de limpieza.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Directorio de datos limpios
DATA_DIR = Path("data/clean")

@st.cache_data
def load_generalidades():
    """Carga datos generales de Casanare."""
    try:
        return pd.read_csv(DATA_DIR / "generalidades.csv")
    except FileNotFoundError:
        st.error("❌ Archivo generalidades.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_sector_economico():
    """Carga datos de sectores económicos."""
    try:
        return pd.read_csv(DATA_DIR / "sector_economico.csv")
    except FileNotFoundError:
        st.error("❌ Archivo sector_economico.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_empresarial():
    """Carga datos empresariales por tamaño."""
    try:
        return pd.read_csv(DATA_DIR / "empresarial.csv")
    except FileNotFoundError:
        st.error("❌ Archivo empresarial.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_empresas_municipio():
    """Carga datos de empresas por municipio."""
    try:
        return pd.read_csv(DATA_DIR / "numero_de_empresas_por_municipi.csv")
    except FileNotFoundError:
        st.error("❌ Archivo numero_de_empresas_por_municipi.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_ciclo_vital():
    """Carga datos de distribución poblacional por ciclo vital."""
    try:
        return pd.read_csv(DATA_DIR / "ciclo_vital.csv")
    except FileNotFoundError:
        st.error("❌ Archivo ciclo_vital.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_graduados():
    """Carga datos de graduados por área de conocimiento."""
    try:
        return pd.read_csv(DATA_DIR / "graduados_profesion.csv")
    except FileNotFoundError:
        st.error("❌ Archivo graduados_profesion.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_desercion():
    """Carga datos de deserción escolar por municipio."""
    try:
        return pd.read_csv(DATA_DIR / "tasa_desercion_sector_oficial.csv")
    except FileNotFoundError:
        st.error("❌ Archivo tasa_desercion_sector_oficial.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_morbilidad():
    """Carga datos de morbilidad."""
    try:
        return pd.read_csv(DATA_DIR / "morbilidad1.csv")
    except FileNotFoundError:
        st.error("❌ Archivo morbilidad1.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_calidad_agua():
    """Carga datos de calidad del agua."""
    try:
        return pd.read_csv(DATA_DIR / "calidad_del_agua.csv")
    except FileNotFoundError:
        st.error("❌ Archivo calidad_del_agua.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_seguridad():
    """Carga datos de seguridad ciudadana."""
    try:
        return pd.read_csv(DATA_DIR / "seguridad.csv")
    except FileNotFoundError:
        st.error("❌ Archivo seguridad.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_estructura_demografica():
    """Carga datos de estructura demográfica."""
    try:
        return pd.read_csv(DATA_DIR / "estructura_demografica.csv")
    except FileNotFoundError:
        st.error("❌ Archivo estructura_demografica.csv no encontrado")
        return pd.DataFrame()

def get_kpi_values():
    """Extrae KPIs principales EXCLUSIVAMENTE desde datos CSV."""
    df_general = load_generalidades()
    
    if df_general.empty:
        st.error("❌ No se pudieron cargar los datos generales. Verifique que el archivo generalidades.csv existe.")
        return {}
    
    kpis = {}
    
    # Extraer valores reales desde CSV
    try:
        for _, row in df_general.iterrows():
            indicador = str(row.iloc[1]).lower()
            valor = row.iloc[3]
            
            if 'poblacion' in indicador and 'total' in indicador:
                kpis['poblacion_2025'] = int(valor) if pd.notna(valor) else 0
            elif 'pib' in indicador and 'departamental' in indicador:
                kpis['pib_2023'] = float(valor) if pd.notna(valor) else 0
            elif 'puntaje' in indicador and 'general' in indicador:
                kpis['puntaje_idc'] = float(valor) if pd.notna(valor) else 0
            elif 'ranking' in indicador:
                kpis['ranking_idc'] = int(valor) if pd.notna(valor) else 0
    except Exception as e:
        st.error(f"❌ Error procesando datos generales: {e}")
        return {}
    
    return kpis

def get_salud_kpis():
    """Extrae KPIs de salud EXCLUSIVAMENTE desde datos CSV."""
    df_demo = load_estructura_demografica()
    
    if df_demo.empty:
        st.error("❌ No se pudieron cargar los datos demográficos. Verifique que el archivo estructura_demografica.csv existe.")
        return {}
    
    kpis = {}
    
    # Extraer valores reales desde CSV
    try:
        for _, row in df_demo.iterrows():
            indicador = str(row.iloc[0]).lower()
            valor = row.iloc[1]
            
            if 'esperanza' in indicador and 'vida' in indicador:
                kpis['esperanza_vida'] = float(valor) if pd.notna(valor) else 0
            elif 'mortalidad' in indicador and 'infantil' in indicador:
                kpis['mortalidad_infantil'] = float(valor) if pd.notna(valor) else 0
            elif 'fecundidad' in indicador and 'adolescente' in indicador:
                kpis['fecundidad_adolescente'] = float(valor) if pd.notna(valor) else 0
    except Exception as e:
        st.error(f"❌ Error procesando datos demográficos: {e}")
        return {}
    
    return kpis

def get_educacion_kpis():
    """Extrae KPIs de educación EXCLUSIVAMENTE desde datos CSV."""
    df_desercion = load_desercion()
    df_graduados = load_graduados()
    
    kpis = {}
    
    # Calcular desde datos reales
    if not df_desercion.empty and 'tasa_desercion' in df_desercion.columns:
        kpis['tasa_desercion_promedio'] = round(df_desercion['tasa_desercion'].mean(), 1)
    else:
        st.warning("⚠️ No se encontraron datos de deserción")
        kpis['tasa_desercion_promedio'] = 0
    
    if not df_graduados.empty and 'numero_de_graduados' in df_graduados.columns:
        kpis['total_graduados'] = int(df_graduados['numero_de_graduados'].sum())
    else:
        st.warning("⚠️ No se encontraron datos de graduados")
        kpis['total_graduados'] = 0
    
    return kpis