"""
Loader optimizado para carga centralizada de datos
Versión 3.1 - Corregido para compatibilidad con el nuevo pipeline de limpieza
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """Cargador centralizado y optimizado de datos para el dashboard."""

    def __init__(self, data_dir: str = "data/clean"):
        self.data_dir = Path(data_dir)
        self._cache: Dict[str, pd.DataFrame] = {}
        self._loaded = False

        # Mapeo de archivos a funciones de carga. Nombres de archivo sanitizados.
        self.file_mappings = {
            'generalidades': 'generalidades.csv',
            'sector_economico': 'sector_economico.csv',
            'empresarial': 'empresarial.csv',
            'graduados': 'graduados_profesion.csv',
            'morbilidad': 'morbilidad1.csv',
            'seguridad': 'seguridad.csv',
            'desercion': 'tasa_desercin_sector_oficial.csv', # Corregido
            'municipios_empresas': 'numero_de_empresas_por_municipi.csv',
            'cultivos': 'cultivos.csv',
            'calidad_agua': 'calidad_del_agua.csv',
            'mortalidad': 'mortalidad1.csv'
        }

    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """Carga, procesa y cachea todos los datasets necesarios para el dashboard."""
        if self._loaded:
            logger.info("📦 Datos ya cargados desde caché.")
            return self._cache

        logger.info("🚀 Cargando y procesando todos los datos...")

        for key, filename in self.file_mappings.items():
            try:
                file_path = self.data_dir / filename
                if not file_path.exists():
                    logger.warning(f"⚠️ Archivo no encontrado: {filename}. Se creará un DataFrame vacío.")
                    self._cache[key] = pd.DataFrame()
                    continue

                df = pd.read_csv(file_path)
                df = self._optimize_dataframe(df, key)
                self._cache[key] = df
                logger.info(f"✅ {key}: {len(df)} registros cargados y optimizados.")

            except Exception as e:
                logger.error(f"❌ Error cargando el archivo {filename} para '{key}': {e}", exc_info=True)
                self._cache[key] = pd.DataFrame()

        self._loaded = True
        logger.info(f"📊 Total de datasets cargados: {len(self._cache)}")
        return self._cache

    def _optimize_dataframe(self, df: pd.DataFrame, key: str) -> pd.DataFrame:
        """Aplica optimizaciones numéricas y de tipos a un DataFrame."""
        df = df.dropna(how='all')

        # Columnas a convertir a numérico (sanitizadas)
        numeric_cols = {
            'generalidades': ['ao', 'valor'],
            'sector_economico': ['participacin_porcentual'],
            'empresarial': ['nmero_de_empresas', 'porcentaje_del_total'],
            'graduados': ['nmero_de_graduados', 'porcentaje_del_total'],
            'morbilidad': ['ao', 'valor'],
            'seguridad': ['valor'],
            'desercion': ['ao', 'tasa_desercin'],
            'mortalidad': ['valor'],
        }

        if key in numeric_cols:
            for col in numeric_cols[key]:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # No dropear NaNs para 'generalidades' ya que la columna 'valor' es mixta
            # y se perderían filas importantes como la del ranking.
            if key != 'generalidades':
                df = df.dropna(subset=numeric_cols[key])

        return df

    def get_data(self, key: str) -> pd.DataFrame:
        """Obtiene un DataFrame específico del caché."""
        if not self._loaded:
            self.load_all_data()
        return self._cache.get(key, pd.DataFrame())

    def get_kpis(self) -> Dict[str, Any]:
        """Extrae los KPIs principales de forma robusta desde el dataset de generalidades."""
        df_general = self.get_data('generalidades')
        if df_general.empty:
            return {}

        kpis = {
            'poblacion': 0,
            'pib': 0,
            'ranking_idc': 0
        }

        # Extraer Población
        pop_row = df_general[df_general['indicador'].str.contains('Población Total', case=False, na=False)]
        if not pop_row.empty:
            kpis['poblacion'] = int(pop_row['valor'].iloc[0])

        # Extraer PIB
        pib_row = df_general[df_general['indicador'].str.contains('PIB Departamental', case=False, na=False)]
        if not pib_row.empty:
            kpis['pib'] = float(pib_row['valor'].iloc[0])

        # Extraer Ranking del IDC
        rank_row = df_general[df_general['indicador'].str.contains('Puntaje General IDC', case=False, na=False)]
        if not rank_row.empty and 'rankingnacional2025' in rank_row.columns:
            # Asegurarse de que el valor no sea nulo antes de convertir a entero
            ranking_value = rank_row['rankingnacional2025'].iloc[0]
            if pd.notna(ranking_value):
                kpis['ranking_idc'] = int(ranking_value)

        return kpis
    
    def get_empresas_total(self) -> int:
        """Calcula el número total de empresas usando el nombre de columna correcto."""
        df_empresas = self.get_data('empresarial')
        # Corregido: usar el nombre de columna sanitizado 'nmero_de_empresas'
        if df_empresas.empty or 'nmero_de_empresas' not in df_empresas.columns:
            return 0
        return int(df_empresas['nmero_de_empresas'].sum())
    
    def get_sectores_economicos(self) -> pd.DataFrame:
        """Obtiene datos de sectores económicos."""
        return self.get_data('sector_economico')
    
    def get_empresas_por_tamano(self) -> pd.DataFrame:
        """Obtiene datos de empresas por tamaño."""
        return self.get_data('empresarial')
    
    def get_graduados_por_area(self) -> pd.DataFrame:
        """Obtiene datos de graduados por área de conocimiento."""
        return self.get_data('graduados') # El nombre de la columna ya está sanitizado
    
    def get_dengue_data(self) -> pd.DataFrame:
        """Filtra y obtiene datos específicos sobre el dengue."""
        df_morbilidad = self.get_data('morbilidad')
        if df_morbilidad.empty or 'indicador' not in df_morbilidad.columns:
            return pd.DataFrame()

        df_morbilidad['indicador'] = df_morbilidad['indicador'].astype(str)
        return df_morbilidad[df_morbilidad['indicador'].str.contains('Dengue', case=False, na=False)]
    
    def get_seguridad_data(self) -> pd.DataFrame:
        """Obtiene datos de seguridad."""
        return self.get_data('seguridad')
    
    def get_cultivos_data(self) -> pd.DataFrame:
        """Obtiene datos de cultivos."""
        return self.get_data('cultivos')
    
    def get_municipios_empresas(self) -> pd.DataFrame:
        """Obtiene datos de empresas por municipio."""
        return self.get_data('municipios_empresas')
    
    def get_desercion_data(self) -> pd.DataFrame:
        """Obtiene datos de deserción escolar."""
        return self.get_data('desercion')
    
    def get_calidad_agua_data(self) -> pd.DataFrame:
        """Obtiene datos de calidad del agua."""
        return self.get_data('calidad_agua')

    def get_mortalidad_data(self) -> pd.DataFrame:
        """Obtiene datos de mortalidad."""
        return self.get_data('mortalidad')

# --- Instancia Singleton ---
# Se crea una única instancia que será compartida por toda la aplicación
data_loader_instance = DataLoader()

def get_data_loader() -> DataLoader:
    """Devuelve la instancia única del DataLoader."""
    return data_loader_instance
