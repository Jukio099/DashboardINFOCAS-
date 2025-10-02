"""
Loader optimizado para carga centralizada de datos
Versión 3.0 - Dashboard de élite para Casanare
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
import warnings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """Cargador centralizado de datos para el dashboard"""
    
    def __init__(self, data_dir: str = "data/clean"):
        self.data_dir = Path(data_dir)
        self._cache = {}
        self._loaded = False
        
        # Mapeo de archivos a funciones de carga
        self.file_mappings = {
            'generalidades': 'generalidades.csv',
            'sector_economico': 'sector_economico.csv',
            'empresarial': 'empresarial.csv',
            'graduados': 'graduados_profesion.csv',
            'morbilidad': 'morbilidad1.csv',
            'seguridad': 'seguridad.csv',
            'desercion': 'tasa_desercion_sector_oficial.csv',
            'municipios_empresas': 'numero_de_empresas_por_municipi.csv',
            'cultivos': 'cultivos.csv',
            'calidad_agua': 'calidad_del_agua.csv'
        }
    
    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """Cargar todos los datos de una vez"""
        if self._loaded:
            logger.info("📦 Datos ya cargados desde caché")
            return self._cache
        
        logger.info("🚀 Cargando todos los datos...")
        
        for key, filename in self.file_mappings.items():
            try:
                file_path = self.data_dir / filename
                if file_path.exists():
                    df = pd.read_csv(file_path)
                    df = df.dropna(how='all')
                    
                    # Optimizaciones específicas por tipo de datos
                    if key == 'sector_economico':
                        df = self._optimize_sector_economico(df)
                    elif key == 'empresarial':
                        df = self._optimize_empresarial(df)
                    elif key == 'graduados':
                        df = self._optimize_graduados(df)
                    elif key == 'morbilidad':
                        df = self._optimize_morbilidad(df)
                    elif key == 'seguridad':
                        df = self._optimize_seguridad(df)
                    elif key == 'desercion':
                        df = self._optimize_desercion(df)
                    elif key == 'generalidades':
                        df = self._optimize_generalidades(df)
                    
                    self._cache[key] = df
                    logger.info(f"✅ {key}: {len(df)} registros cargados")
                else:
                    logger.warning(f"⚠️ Archivo no encontrado: {filename}")
                    self._cache[key] = pd.DataFrame()
                    
            except Exception as e:
                logger.error(f"❌ Error cargando {key}: {e}")
                self._cache[key] = pd.DataFrame()
        
        self._loaded = True
        logger.info(f"📊 Total de datasets cargados: {len(self._cache)}")
        return self._cache
    
    def _optimize_sector_economico(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optimizar datos del sector económico"""
        # Asegurar que participacion_porcentual sea float
        if 'participacion_porcentual' in df.columns:
            df['participacion_porcentual'] = pd.to_numeric(df['participacion_porcentual'], errors='coerce')
        
        # Filtrar solo sectores con participación válida
        df = df[df['participacion_porcentual'].notna()]
        df = df[df['participacion_porcentual'] > 0]
        
        return df
    
    def _optimize_empresarial(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optimizar datos empresariales"""
        # Asegurar que numero_de_empresas sea int
        if 'numero_de_empresas' in df.columns:
            df['numero_de_empresas'] = pd.to_numeric(df['numero_de_empresas'], errors='coerce')
        
        # Asegurar que porcentaje_del_total sea float
        if 'porcentaje_del_total' in df.columns:
            df['porcentaje_del_total'] = pd.to_numeric(df['porcentaje_del_total'], errors='coerce')
        
        # Filtrar solo empresas con datos válidos
        df = df[df['numero_de_empresas'].notna()]
        df = df[df['numero_de_empresas'] > 0]
        
        return df
    
    def _optimize_graduados(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optimizar datos de graduados"""
        # Asegurar que número_de_graduados sea int (con tilde)
        if 'número_de_graduados' in df.columns:
            df['número_de_graduados'] = pd.to_numeric(df['número_de_graduados'], errors='coerce')
        
        # Asegurar que porcentaje_del_total sea float
        if 'porcentaje_del_total' in df.columns:
            df['porcentaje_del_total'] = pd.to_numeric(df['porcentaje_del_total'], errors='coerce')
        
        # Filtrar solo graduados con datos válidos
        df = df[df['número_de_graduados'].notna()]
        df = df[df['número_de_graduados'] > 0]
        
        return df
    
    def _optimize_morbilidad(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optimizar datos de morbilidad"""
        # Asegurar que año sea int
        if 'a_o' in df.columns:
            df['a_o'] = pd.to_numeric(df['a_o'], errors='coerce')
        
        # Asegurar que valor sea int
        if 'valor' in df.columns:
            df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
        
        # Filtrar solo datos válidos
        df = df[df['a_o'].notna()]
        df = df[df['valor'].notna()]
        
        return df
    
    def _optimize_seguridad(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optimizar datos de seguridad"""
        # Los datos de seguridad tienen estructura diferente: indicador, valor, etc.
        # Asegurar que valor sea int
        if 'valor' in df.columns:
            df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
        
        # Filtrar solo datos válidos
        df = df[df['valor'].notna()]
        df = df[df['valor'] > 0]
        
        return df
    
    def _optimize_desercion(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optimizar datos de deserción"""
        # Asegurar que ano sea int (sin tilde)
        if 'ano' in df.columns:
            df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
        
        # Asegurar que tasa_desercion sea float
        if 'tasa_desercion' in df.columns:
            df['tasa_desercion'] = pd.to_numeric(df['tasa_desercion'], errors='coerce')
        
        # Filtrar solo datos válidos
        df = df[df['ano'].notna()]
        df = df[df['tasa_desercion'].notna()]
        
        return df
    
    def _optimize_generalidades(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optimizar datos generales"""
        # Asegurar que a_o sea int (no año)
        if 'a_o' in df.columns:
            df['a_o'] = pd.to_numeric(df['a_o'], errors='coerce')
        
        # Asegurar que valor sea float
        if 'valor' in df.columns:
            df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
        
        # Filtrar solo datos válidos
        df = df[df['a_o'].notna()]
        df = df[df['valor'].notna()]
        
        return df
    
    def get_data(self, key: str) -> pd.DataFrame:
        """Obtener datos específicos"""
        if not self._loaded:
            self.load_all_data()
        
        return self._cache.get(key, pd.DataFrame())
    
    def get_kpis(self) -> Dict[str, any]:
        """Extraer KPIs principales"""
        df_general = self.get_data('generalidades')
        
        if df_general.empty:
            return {}
        
        kpis = {}
        
        for _, row in df_general.iterrows():
            indicador = str(row.get('indicador', '')).lower()
            valor = row.get('valor', 0)
            
            if 'población' in indicador and 'total' in indicador:
                kpis['poblacion'] = int(valor) if pd.notna(valor) else 0
            elif 'pib' in indicador and 'departamental' in indicador:
                kpis['pib'] = float(valor) if pd.notna(valor) else 0
            elif 'puntaje' in indicador and 'general' in indicador:
                kpis['puntaje_idc'] = float(valor) if pd.notna(valor) else 0
            elif 'ranking' in indicador:
                ranking_val = row.get('rankingnacional2025', 0)
                kpis['ranking_idc'] = int(ranking_val) if pd.notna(ranking_val) else 0
        
        return kpis
    
    def get_empresas_total(self) -> int:
        """Calcular total de empresas"""
        df_empresas = self.get_data('empresarial')
        if df_empresas.empty:
            return 0
        
        try:
            total = df_empresas['numero_de_empresas'].sum()
            return int(total) if pd.notna(total) else 0
        except Exception as e:
            logger.error(f"Error calculando total de empresas: {e}")
            return 0
    
    def get_sectores_economicos(self) -> pd.DataFrame:
        """Obtener datos de sectores económicos optimizados"""
        return self.get_data('sector_economico')
    
    def get_empresas_por_tamano(self) -> pd.DataFrame:
        """Obtener datos de empresas por tamaño"""
        return self.get_data('empresarial')
    
    def get_graduados_por_area(self) -> pd.DataFrame:
        """Obtener datos de graduados por área"""
        df = self.get_data('graduados')
        # Renombrar columnas para compatibilidad
        if not df.empty and 'área_de_conocimiento' in df.columns:
            df = df.rename(columns={'área_de_conocimiento': 'area_de_conocimiento'})
        return df
    
    def get_dengue_data(self) -> pd.DataFrame:
        """Obtener datos de dengue"""
        df_morbilidad = self.get_data('morbilidad')
        if df_morbilidad.empty:
            return pd.DataFrame()
        
        # Filtrar datos de dengue
        try:
            df_morbilidad['indicador'] = df_morbilidad['indicador'].astype(str)
            df_dengue = df_morbilidad[df_morbilidad['indicador'].str.contains('Dengue', case=False, na=False)]
            return df_dengue
        except Exception as e:
            logger.error(f"Error filtrando datos de dengue: {e}")
            return pd.DataFrame()
    
    def get_seguridad_data(self) -> pd.DataFrame:
        """Obtener datos de seguridad"""
        return self.get_data('seguridad')
    
    def get_cultivos_data(self) -> pd.DataFrame:
        """Obtener datos de cultivos"""
        return self.get_data('cultivos')
    
    def get_municipios_empresas(self) -> pd.DataFrame:
        """Obtener datos de empresas por municipio"""
        return self.get_data('municipios_empresas')
    
    def get_desercion_data(self) -> pd.DataFrame:
        """Obtener datos de deserción"""
        return self.get_data('desercion')
    
    def get_municipios_empresas(self) -> pd.DataFrame:
        """Obtener datos de empresas por municipio"""
        return self.get_data('municipios_empresas')
    
    def get_cultivos_data(self) -> pd.DataFrame:
        """Obtener datos de cultivos"""
        return self.get_data('cultivos')
    
    def get_calidad_agua_data(self) -> pd.DataFrame:
        """Obtener datos de calidad del agua"""
        return self.get_data('calidad_agua')

# Instancia global del cargador
data_loader = DataLoader()

def get_data_loader() -> DataLoader:
    """Obtener instancia del cargador de datos"""
    return data_loader
