"""
Modelo base para todos los modelos de datos.
Define funcionalidades comunes y validadores base.
"""

from typing import Any, Optional
from pydantic import BaseModel, Field, validator
import pandas as pd


class BaseDataModel(BaseModel):
    """Modelo base para todos los modelos de datos del dashboard."""
    
    class Config:
        """Configuración del modelo."""
        validate_assignment = True
        extra = "forbid"  # No permitir campos adicionales
        str_strip_whitespace = True  # Eliminar espacios en blanco
    
    @validator('*', pre=True)
    def clean_strings(cls, v):
        """Limpia strings eliminando espacios y convirtiendo valores vacíos a None."""
        if isinstance(v, str):
            # Eliminar espacios y convertir strings vacíos a None
            cleaned = v.strip()
            if cleaned in ['', 'N/A', 'n/a', 'NULL', 'null', '-']:
                return None
            return cleaned
        return v
    
    @validator('*', pre=True)
    def clean_numbers(cls, v):
        """Limpia números convirtiendo comas a puntos y manejando valores vacíos."""
        if isinstance(v, str) and v.strip():
            # Reemplazar comas por puntos para decimales
            cleaned = v.replace(',', '.').strip()
            if cleaned in ['', 'N/A', 'n/a', 'NULL', 'null', '-']:
                return None
            return cleaned
        return v


class ValidationResult:
    """Resultado de la validación de un modelo."""
    
    def __init__(self, is_valid: bool, data: Optional[pd.DataFrame] = None, errors: list = None):
        self.is_valid = is_valid
        self.data = data
        self.errors = errors or []
    
    def add_error(self, row_index: int, field: str, value: Any, error_message: str):
        """Añade un error de validación."""
        self.errors.append({
            'row_index': row_index,
            'field': field,
            'value': value,
            'error': error_message
        })
    
    def has_errors(self) -> bool:
        """Verifica si hay errores."""
        return len(self.errors) > 0
    
    def get_error_summary(self) -> str:
        """Obtiene un resumen de errores."""
        if not self.errors:
            return "Sin errores"
        
        summary = f"Total de errores: {len(self.errors)}\n"
        for error in self.errors[:5]:  # Mostrar solo los primeros 5
            summary += f"  Fila {error['row_index']}: {error['field']} = '{error['value']}' - {error['error']}\n"
        
        if len(self.errors) > 5:
            summary += f"  ... y {len(self.errors) - 5} errores más"
        
        return summary
