"""
Lector de archivos Excel con manejo robusto de errores.
"""

import pandas as pd
from typing import Dict, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ExcelReader:
    """Lector robusto de archivos Excel."""
    
    def __init__(self, file_path: str):
        """
        Inicializar el lector de Excel.
        
        Args:
            file_path: Ruta al archivo Excel
        """
        self.file_path = Path(file_path)
        self.sheets_data = {}
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
    
    def read_all_sheets(self) -> Dict[str, pd.DataFrame]:
        """
        Lee todas las hojas del archivo Excel.
        
        Returns:
            Dict[str, pd.DataFrame]: Diccionario con nombre de hoja y DataFrame
        """
        logger.info(f"Leyendo archivo Excel: {self.file_path}")
        
        try:
            # Leer todas las hojas
            excel_file = pd.ExcelFile(self.file_path)
            sheet_names = excel_file.sheet_names
            
            logger.info(f"Hojas encontradas: {sheet_names}")
            
            for sheet_name in sheet_names:
                try:
                    # Leer la hoja
                    df = pd.read_excel(self.file_path, sheet_name=sheet_name)
                    
                    # Limpiar nombres de columnas
                    df.columns = df.columns.str.strip()
                    
                    # Eliminar filas completamente vacías
                    df = df.dropna(how='all')
                    
                    # Eliminar columnas completamente vacías
                    df = df.dropna(axis=1, how='all')
                    
                    if not df.empty:
                        self.sheets_data[sheet_name] = df
                        logger.info(f"Hoja '{sheet_name}': {len(df)} filas, {len(df.columns)} columnas")
                    else:
                        logger.warning(f"Hoja '{sheet_name}' está vacía")
                
                except Exception as e:
                    logger.error(f"Error leyendo hoja '{sheet_name}': {e}")
                    continue
            
            logger.info(f"Total de hojas leídas: {len(self.sheets_data)}")
            return self.sheets_data
            
        except Exception as e:
            logger.error(f"Error leyendo archivo Excel: {e}")
            raise
    
    def get_sheet_info(self) -> Dict[str, Dict]:
        """Obtiene información detallada de cada hoja."""
        info = {}
        
        for sheet_name, df in self.sheets_data.items():
            info[sheet_name] = {
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': list(df.columns),
                'memory_usage': df.memory_usage(deep=True).sum(),
                'dtypes': df.dtypes.to_dict(),
                'null_counts': df.isnull().sum().to_dict()
            }
        
        return info
    
    def print_summary(self):
        """Imprime un resumen de las hojas leídas."""
        print("=== RESUMEN DE HOJAS DE EXCEL ===\n")
        
        for sheet_name, df in self.sheets_data.items():
            print(f"📊 {sheet_name}")
            print(f"   Filas: {len(df)}")
            print(f"   Columnas: {len(df.columns)}")
            print(f"   Columnas: {', '.join(df.columns)}")
            print(f"   Valores nulos: {df.isnull().sum().sum()}")
            print()
    
    def get_sheet(self, sheet_name: str) -> Optional[pd.DataFrame]:
        """Obtiene una hoja específica."""
        return self.sheets_data.get(sheet_name)
