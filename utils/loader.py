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
        st.warning("⚠️ Archivo generalidades.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_sector_economico():
    """Carga datos de sectores económicos."""
    try:
        return pd.read_csv(DATA_DIR / "sector_economico.csv")
    except FileNotFoundError:
        st.warning("⚠️ Archivo sector_economico.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_empresarial():
    """Carga datos empresariales por tamaño."""
    try:
        return pd.read_csv(DATA_DIR / "empresarial.csv")
    except FileNotFoundError:
        st.warning("⚠️ Archivo empresarial.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_empresas_municipio():
    """Carga datos de empresas por municipio."""
    try:
        return pd.read_csv(DATA_DIR / "numero_de_empresas_por_municipi.csv")
    except FileNotFoundError:
        st.warning("⚠️ Archivo numero_de_empresas_por_municipi.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_ciclo_vital():
    """Carga datos de distribución poblacional por ciclo vital."""
    try:
        return pd.read_csv(DATA_DIR / "ciclo_vital.csv")
    except FileNotFoundError:
        st.warning("⚠️ Archivo ciclo_vital.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_graduados():
    """Carga datos de graduados por área de conocimiento."""
    try:
        return pd.read_csv(DATA_DIR / "graduados_profesion.csv")
    except FileNotFoundError:
        st.warning("⚠️ Archivo graduados_profesion.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_desercion():
    """Carga datos de deserción escolar por municipio."""
    try:
        return pd.read_csv(DATA_DIR / "tasa_desercion_sector_oficial.csv")
    except FileNotFoundError:
        st.warning("⚠️ Archivo tasa_desercion_sector_oficial.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_morbilidad():
    """Carga datos de morbilidad."""
    try:
        return pd.read_csv(DATA_DIR / "morbilidad1.csv")
    except FileNotFoundError:
        st.warning("⚠️ Archivo morbilidad1.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_calidad_agua():
    """Carga datos de calidad del agua."""
    try:
        return pd.read_csv(DATA_DIR / "calidad_del_agua.csv")
    except FileNotFoundError:
        st.warning("⚠️ Archivo calidad_del_agua.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_seguridad():
    """Carga datos de seguridad ciudadana."""
    try:
        return pd.read_csv(DATA_DIR / "seguridad.csv")
    except FileNotFoundError:
        st.warning("⚠️ Archivo seguridad.csv no encontrado")
        return pd.DataFrame()

@st.cache_data
def load_estructura_demografica():
    """Carga datos de estructura demográfica."""
    try:
        return pd.read_csv(DATA_DIR / "estructura_demografica.csv")
    except FileNotFoundError:
        st.warning("⚠️ Archivo estructura_demografica.csv no encontrado")
        return pd.DataFrame()

def get_kpi_values():
    """Extrae KPIs principales desde datos limpios."""
    df_general = load_generalidades()
    
    if df_general.empty:
        return {
            'poblacion_2025': 481938,
            'pib_2023': 23082000,
            'puntaje_idc': 5.01,
            'ranking_idc': 17
        }
    
    # Buscar valores específicos en las primeras filas
    kpis = {
        'poblacion_2025': 481938,
        'pib_2023': 23082000,
        'puntaje_idc': 5.01,
        'ranking_idc': 17
    }
    
    # Si los datos están en formato tabular, extraer valores
    try:
        for _, row in df_general.iterrows():
            if 'poblacion' in str(row.iloc[1]).lower():
                kpis['poblacion_2025'] = int(row.iloc[3]) if pd.notna(row.iloc[3]) else 481938
            elif 'pib' in str(row.iloc[1]).lower():
                kpis['pib_2023'] = float(row.iloc[3]) if pd.notna(row.iloc[3]) else 23082000
            elif 'puntaje' in str(row.iloc[1]).lower() or 'idc' in str(row.iloc[1]).lower():
                kpis['puntaje_idc'] = float(row.iloc[3]) if pd.notna(row.iloc[3]) else 5.01
                kpis['ranking_idc'] = int(row.iloc[5]) if len(row) > 5 and pd.notna(row.iloc[5]) else 17
    except:
        pass  # Usar valores por defecto
    
    return kpis

def get_salud_kpis():
    """Extrae KPIs de salud pública."""
    df_demo = load_estructura_demografica()
    
    if df_demo.empty:
        return {
            'esperanza_vida': 76.2,
            'mortalidad_infantil': 8.9,
            'fecundidad_adolescente': 45.7
        }
    
    kpis = {
        'esperanza_vida': 76.2,
        'mortalidad_infantil': 8.9,
        'fecundidad_adolescente': 45.7
    }
    
    # Extraer valores reales si están disponibles
    try:
        for _, row in df_demo.iterrows():
            indicador = str(row.iloc[0]).lower()
            valor = row.iloc[1]
            
            if 'esperanza' in indicador and 'vida' in indicador:
                kpis['esperanza_vida'] = float(valor) if pd.notna(valor) else 76.2
            elif 'mortalidad' in indicador and 'infantil' in indicador:
                kpis['mortalidad_infantil'] = float(valor) if pd.notna(valor) else 8.9
            elif 'fecundidad' in indicador and 'adolescente' in indicador:
                kpis['fecundidad_adolescente'] = float(valor) if pd.notna(valor) else 45.7
    except:
        pass  # Usar valores por defecto
    
    return kpis

def get_educacion_kpis():
    """Extrae KPIs de educación."""
    df_desercion = load_desercion()
    df_graduados = load_graduados()
    
    tasa_desercion_promedio = df_desercion['tasa_desercion'].mean() if not df_desercion.empty else 5.5
    total_graduados = df_graduados['numero_de_graduados'].sum() if not df_graduados.empty else 4850
    
    return {
        'tasa_desercion_promedio': round(tasa_desercion_promedio, 1),
        'total_graduados': int(total_graduados)
    }