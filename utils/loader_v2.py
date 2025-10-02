"""
Sistema de carga de datos v2.0
Optimizado para usar datos validados con Pydantic.

Este módulo reemplaza loader.py con un sistema más robusto que:
- Confía en la validación previa de los datos
- Elimina validaciones redundantes
- Mejora el rendimiento
- Proporciona mejor manejo de errores
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

# Directorio de datos limpios
DATA_DIR = Path("data/clean")


class DataLoader:
    """Cargador de datos optimizado para datos validados."""
    
    def __init__(self, data_dir: str = "data/clean"):
        """
        Inicializar el cargador.
        
        Args:
            data_dir: Directorio con datos limpios
        """
        self.data_dir = Path(data_dir)
        self._cache = {}
        
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Directorio de datos no encontrado: {data_dir}")
    
    @st.cache_data
    def load_csv(_self, _filename: str) -> pd.DataFrame:
        """
        Carga un archivo CSV con cache.
        
        Args:
            _filename: Nombre del archivo CSV
            
        Returns:
            pd.DataFrame: Datos cargados
        """
        file_path = _self.data_dir / _filename
        
        if not file_path.exists():
            logger.warning(f"Archivo no encontrado: {file_path}")
            return pd.DataFrame()
        
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Datos cargados: {_filename} - {len(df)} registros")
            return df
            
        except Exception as e:
            logger.error(f"Error cargando {_filename}: {e}")
            return pd.DataFrame()
    
    def get_available_files(self) -> list:
        """Obtiene lista de archivos CSV disponibles."""
        return [f.name for f in self.data_dir.glob("*.csv")]
    
    def get_file_info(self, filename: str) -> Dict[str, Any]:
        """Obtiene información detallada de un archivo."""
        file_path = self.data_dir / filename
        
        if not file_path.exists():
            return {"error": "Archivo no encontrado"}
        
        try:
            df = pd.read_csv(file_path)
            return {
                "filename": filename,
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": list(df.columns),
                "memory_usage": df.memory_usage(deep=True).sum(),
                "file_size": file_path.stat().st_size,
                "last_modified": file_path.stat().st_mtime
            }
        except Exception as e:
            return {"error": str(e)}


# Instancia global del cargador
_loader = DataLoader()


# Funciones de carga optimizadas
@st.cache_data
def load_generalidades() -> pd.DataFrame:
    """Carga datos generales de Casanare."""
    return _loader.load_csv("generalidades.csv")


@st.cache_data
def load_sector_economico() -> pd.DataFrame:
    """Carga datos de sectores económicos."""
    return _loader.load_csv("sector_economico.csv")


@st.cache_data
def load_empresarial() -> pd.DataFrame:
    """Carga datos empresariales por tamaño."""
    return _loader.load_csv("empresarial.csv")


@st.cache_data
def load_empresas_municipio() -> pd.DataFrame:
    """Carga datos de empresas por municipio."""
    return _loader.load_csv("numero_de_empresas_por_municipi.csv")


@st.cache_data
def load_ciclo_vital() -> pd.DataFrame:
    """Carga datos de distribución poblacional por ciclo vital."""
    return _loader.load_csv("ciclo_vital.csv")


@st.cache_data
def load_graduados() -> pd.DataFrame:
    """Carga datos de graduados por área de conocimiento."""
    return _loader.load_csv("graduados_profesion.csv")


@st.cache_data
def load_desercion() -> pd.DataFrame:
    """Carga datos de deserción escolar por municipio."""
    return _loader.load_csv("tasa_desercion_sector_oficial.csv")


@st.cache_data
def load_morbilidad() -> pd.DataFrame:
    """Carga datos de morbilidad."""
    return _loader.load_csv("morbilidad1.csv")


@st.cache_data
def load_calidad_agua() -> pd.DataFrame:
    """Carga datos de calidad del agua."""
    return _loader.load_csv("calidad_del_agua.csv")


@st.cache_data
def load_seguridad() -> pd.DataFrame:
    """Carga datos de seguridad ciudadana."""
    return _loader.load_csv("seguridad.csv")


@st.cache_data
def load_estructura_demografica() -> pd.DataFrame:
    """Carga datos de estructura demográfica."""
    return _loader.load_csv("estructura_demografica.csv")


# Funciones de KPIs optimizadas
@st.cache_data
def get_kpi_values() -> Dict[str, Any]:
    """Extrae KPIs principales desde datos validados."""
    df_general = load_generalidades()
    
    if df_general.empty:
        logger.warning("No se pudieron cargar los datos generales")
        return {}
    
    kpis = {}
    
    try:
        for _, row in df_general.iterrows():
            indicador = str(row.get('indicador', '')).lower()
            valor = row.get('valor')
            
            if 'poblacion' in indicador and 'total' in indicador:
                kpis['poblacion_2025'] = int(valor) if pd.notna(valor) else 0
            elif 'pib' in indicador and 'departamental' in indicador:
                kpis['pib_2023'] = float(valor) if pd.notna(valor) else 0
            elif 'puntaje' in indicador and 'general' in indicador:
                kpis['puntaje_idc'] = float(valor) if pd.notna(valor) else 0
            elif 'ranking' in indicador:
                kpis['ranking_idc'] = int(valor) if pd.notna(valor) else 0
                
    except Exception as e:
        logger.error(f"Error procesando KPIs: {e}")
        return {}
    
    return kpis


@st.cache_data
def get_salud_kpis() -> Dict[str, Any]:
    """Extrae KPIs de salud desde datos validados."""
    df_demo = load_estructura_demografica()
    
    if df_demo.empty:
        logger.warning("No se pudieron cargar los datos demográficos")
        return {}
    
    kpis = {}
    
    try:
        for _, row in df_demo.iterrows():
            indicador = str(row.get('indicador', '')).lower()
            valor = row.get('valor')
            
            if 'esperanza' in indicador and 'vida' in indicador:
                kpis['esperanza_vida'] = float(valor) if pd.notna(valor) else 0
            elif 'mortalidad' in indicador and 'infantil' in indicador:
                kpis['mortalidad_infantil'] = float(valor) if pd.notna(valor) else 0
            elif 'fecundidad' in indicador and 'adolescente' in indicador:
                kpis['fecundidad_adolescente'] = float(valor) if pd.notna(valor) else 0
                
    except Exception as e:
        logger.error(f"Error procesando KPIs de salud: {e}")
        return {}
    
    return kpis


@st.cache_data
def get_educacion_kpis() -> Dict[str, Any]:
    """Extrae KPIs de educación desde datos validados."""
    df_desercion = load_desercion()
    df_graduados = load_graduados()
    
    kpis = {}
    
    try:
        # Calcular desde datos reales
        if not df_desercion.empty and 'tasa_desercion' in df_desercion.columns:
            kpis['tasa_desercion_promedio'] = round(df_desercion['tasa_desercion'].mean(), 1)
        else:
            kpis['tasa_desercion_promedio'] = 0
        
        if not df_graduados.empty and 'numero_de_graduados' in df_graduados.columns:
            kpis['total_graduados'] = int(df_graduados['numero_de_graduados'].sum())
        else:
            kpis['total_graduados'] = 0
            
    except Exception as e:
        logger.error(f"Error procesando KPIs de educación: {e}")
        return {}
    
    return kpis


@st.cache_data
def get_all_data_summary() -> Dict[str, Any]:
    """Obtiene un resumen de todos los datos disponibles."""
    summary = {
        "available_files": _loader.get_available_files(),
        "data_info": {}
    }
    
    for filename in summary["available_files"]:
        info = _loader.get_file_info(filename)
        summary["data_info"][filename] = info
    
    return summary


# Funciones de compatibilidad con el sistema anterior
def load_all_data() -> Dict[str, pd.DataFrame]:
    """Carga todos los datos disponibles."""
    return {
        'general': load_generalidades(),
        'sector': load_sector_economico(),
        'empresarial': load_empresarial(),
        'municipios': load_empresas_municipio(),
        'ciclo_vital': load_ciclo_vital(),
        'graduados': load_graduados(),
        'desercion': load_desercion(),
        'morbilidad': load_morbilidad(),
        'calidad_agua': load_calidad_agua(),
        'seguridad': load_seguridad(),
        'estructura_demografica': load_estructura_demografica()
    }
