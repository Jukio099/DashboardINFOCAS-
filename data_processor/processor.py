"""
Procesador principal de datos que coordina la lectura y validación.
"""

import pandas as pd
from typing import Dict, Optional
import logging
from pathlib import Path

from .excel_reader import ExcelReader
from .validator import DataValidator

logger = logging.getLogger(__name__)


class DataProcessor:
    """Procesador principal de datos."""
    
    def __init__(self, excel_file_path: str, output_dir: str = "data/clean"):
        """
        Inicializar el procesador.
        
        Args:
            excel_file_path: Ruta al archivo Excel
            output_dir: Directorio de salida para datos limpios
        """
        self.excel_file_path = excel_file_path
        self.output_dir = Path(output_dir)
        self.reader = ExcelReader(excel_file_path)
        self.validator = DataValidator()
        self.processed_data = {}
    
    def process(self, save_clean_data: bool = True) -> Dict[str, pd.DataFrame]:
        """
        Procesa completamente los datos del Excel.
        
        Args:
            save_clean_data: Si guardar los datos limpios como CSV
            
        Returns:
            Dict[str, pd.DataFrame]: Datos procesados y validados
        """
        logger.info("=== INICIANDO PROCESAMIENTO DE DATOS ===")
        
        try:
            # 1. Leer todas las hojas del Excel
            logger.info("Paso 1: Leyendo archivo Excel...")
            sheets_data = self.reader.read_all_sheets()
            
            if not sheets_data:
                raise ValueError("No se pudieron leer hojas del archivo Excel")
            
            # Mostrar resumen de lectura
            self.reader.print_summary()
            
            # 2. Validar todas las hojas
            logger.info("Paso 2: Validando datos...")
            validation_results = self.validator.validate_all_sheets(sheets_data)
            
            # Mostrar resumen de validación
            print(self.validator.get_validation_summary())
            
            # 3. Obtener datos limpios
            logger.info("Paso 3: Obteniendo datos limpios...")
            self.processed_data = self.validator.get_clean_data()
            
            # 4. Guardar datos limpios si se solicita
            if save_clean_data and self.processed_data:
                logger.info("Paso 4: Guardando datos limpios...")
                self.validator.save_clean_data(str(self.output_dir))
                logger.info(f"Datos guardados en: {self.output_dir}")
            
            logger.info("=== PROCESAMIENTO COMPLETADO ===")
            return self.processed_data
            
        except Exception as e:
            logger.error(f"Error en el procesamiento: {e}")
            raise
    
    def get_processed_data(self) -> Dict[str, pd.DataFrame]:
        """Obtiene los datos procesados."""
        return self.processed_data
    
    def get_validation_results(self) -> Dict:
        """Obtiene los resultados de validación."""
        return self.validator.validation_results
    
    def get_processing_summary(self) -> str:
        """Obtiene un resumen completo del procesamiento."""
        summary = "=== RESUMEN DE PROCESAMIENTO ===\n\n"
        
        # Información del archivo
        summary += f"Archivo Excel: {self.excel_file_path}\n"
        summary += f"Directorio de salida: {self.output_dir}\n\n"
        
        # Información de lectura
        sheet_info = self.reader.get_sheet_info()
        summary += f"Hojas procesadas: {len(sheet_info)}\n"
        
        for sheet_name, info in sheet_info.items():
            summary += f"  {sheet_name}: {info['rows']} filas, {info['columns']} columnas\n"
        
        summary += "\n"
        
        # Información de validación
        validation_summary = self.validator.get_validation_summary()
        summary += validation_summary
        
        return summary
    
    def validate_single_sheet(self, sheet_name: str) -> Optional[pd.DataFrame]:
        """Valida una sola hoja y retorna los datos limpios."""
        sheet_data = self.reader.get_sheet(sheet_name)
        
        if sheet_data is None:
            logger.error(f"Hoja '{sheet_name}' no encontrada")
            return None
        
        validation_result = self.validator.validate_sheet(sheet_name, sheet_data)
        
        if validation_result.is_valid:
            return validation_result.data
        else:
            logger.error(f"Validación falló para '{sheet_name}': {validation_result.get_error_summary()}")
            return None
