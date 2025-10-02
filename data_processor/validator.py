"""
Sistema de validación de datos usando modelos Pydantic.
"""

import pandas as pd
from typing import Dict, List, Type, Any, Optional
from pydantic import ValidationError
import logging

from models.base import BaseDataModel, ValidationResult
from models import (
    GeneralidadesModel, SectorEconomicoModel, EmpresarialModel,
    CicloVitalModel, MunicipiosModel, SeguridadModel, MorbilidadModel,
    GraduadosModel, DesercionModel, EstructuraDemograficaModel, CalidadAguaModel
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataValidator:
    """Validador de datos usando modelos Pydantic."""
    
    # Mapeo de hojas de Excel a modelos Pydantic
    SHEET_MODEL_MAPPING = {
        'generalidades': GeneralidadesModel,
        'sector_economico': SectorEconomicoModel,
        'empresarial': EmpresarialModel,
        'ciclo_vital': CicloVitalModel,
        'municipios': MunicipiosModel,
        'seguridad': SeguridadModel,
        'morbilidad': MorbilidadModel,
        'graduados': GraduadosModel,
        'desercion': DesercionModel,
        'estructura_demografica': EstructuraDemograficaModel,
        'calidad_agua': CalidadAguaModel
    }
    
    def __init__(self):
        """Inicializar el validador."""
        self.validation_results = {}
        self.clean_data = {}
    
    def validate_sheet(self, sheet_name: str, df: pd.DataFrame) -> ValidationResult:
        """
        Valida una hoja de Excel contra su modelo correspondiente.
        
        Args:
            sheet_name: Nombre de la hoja
            df: DataFrame con los datos
            
        Returns:
            ValidationResult: Resultado de la validación
        """
        logger.info(f"Validando hoja: {sheet_name}")
        
        # Obtener el modelo correspondiente
        model_class = self.SHEET_MODEL_MAPPING.get(sheet_name)
        if not model_class:
            logger.warning(f"No hay modelo definido para la hoja: {sheet_name}")
            return ValidationResult(
                is_valid=False,
                errors=[{
                    'row_index': 0,
                    'field': 'sheet_name',
                    'value': sheet_name,
                    'error': f'No hay modelo definido para la hoja: {sheet_name}'
                }]
            )
        
        validation_result = ValidationResult(is_valid=True)
        validated_data = []
        
        # Validar cada fila
        for index, row in df.iterrows():
            try:
                # Convertir la fila a diccionario
                row_dict = row.to_dict()
                
                # Validar contra el modelo
                validated_row = model_class(**row_dict)
                validated_data.append(validated_row.dict())
                
            except ValidationError as e:
                validation_result.is_valid = False
                
                # Procesar errores de validación
                for error in e.errors():
                    field = error['loc'][0] if error['loc'] else 'unknown'
                    value = row_dict.get(field, 'N/A')
                    
                    validation_result.add_error(
                        row_index=index,
                        field=field,
                        value=value,
                        error_message=error['msg']
                    )
                
                logger.warning(f"Error en fila {index} de {sheet_name}: {e}")
            
            except Exception as e:
                validation_result.is_valid = False
                validation_result.add_error(
                    row_index=index,
                    field='general',
                    value=str(row_dict),
                    error_message=f'Error inesperado: {str(e)}'
                )
                logger.error(f"Error inesperado en fila {index} de {sheet_name}: {e}")
        
        # Si hay datos válidos, crear DataFrame
        if validated_data:
            validation_result.data = pd.DataFrame(validated_data)
            logger.info(f"Validación exitosa para {sheet_name}: {len(validated_data)} registros")
        else:
            validation_result.is_valid = False
            logger.error(f"No se pudieron validar datos para {sheet_name}")
        
        return validation_result
    
    def validate_all_sheets(self, sheets_data: Dict[str, pd.DataFrame]) -> Dict[str, ValidationResult]:
        """
        Valida todas las hojas de Excel.
        
        Args:
            sheets_data: Diccionario con nombre de hoja y DataFrame
            
        Returns:
            Dict[str, ValidationResult]: Resultados de validación por hoja
        """
        logger.info(f"Validando {len(sheets_data)} hojas de Excel")
        
        results = {}
        
        for sheet_name, df in sheets_data.items():
            result = self.validate_sheet(sheet_name, df)
            results[sheet_name] = result
            
            # Guardar datos limpios si la validación fue exitosa
            if result.is_valid and result.data is not None:
                self.clean_data[sheet_name] = result.data
        
        # Guardar resultados
        self.validation_results = results
        
        return results
    
    def get_validation_summary(self) -> str:
        """Obtiene un resumen de todas las validaciones."""
        summary = "=== RESUMEN DE VALIDACIÓN ===\n\n"
        
        total_sheets = len(self.validation_results)
        valid_sheets = sum(1 for result in self.validation_results.values() if result.is_valid)
        
        summary += f"Total de hojas: {total_sheets}\n"
        summary += f"Hojas válidas: {valid_sheets}\n"
        summary += f"Hojas con errores: {total_sheets - valid_sheets}\n\n"
        
        for sheet_name, result in self.validation_results.items():
            status = "✅ VÁLIDA" if result.is_valid else "❌ CON ERRORES"
            summary += f"{sheet_name}: {status}\n"
            
            if not result.is_valid:
                summary += f"  {result.get_error_summary()}\n"
            
            summary += "\n"
        
        return summary
    
    def save_clean_data(self, output_dir: str = "data/clean"):
        """Guarda los datos limpios como archivos CSV."""
        import os
        
        # Crear directorio si no existe
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info(f"Guardando datos limpios en {output_dir}")
        
        for sheet_name, df in self.clean_data.items():
            output_file = os.path.join(output_dir, f"{sheet_name}.csv")
            df.to_csv(output_file, index=False)
            logger.info(f"Guardado: {output_file}")
    
    def get_clean_data(self) -> Dict[str, pd.DataFrame]:
        """Obtiene los datos limpios validados."""
        return self.clean_data
