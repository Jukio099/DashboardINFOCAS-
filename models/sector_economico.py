"""
Modelo Pydantic para validación de datos del sector económico
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
import re

class SectorEconomico(BaseModel):
    """Modelo para validar datos del sector económico"""
    
    sector_economico: str = Field(..., description="Nombre del sector económico")
    participacion_porcentual: float = Field(..., ge=0, le=100, description="Participación porcentual del sector")
    valor_aproximado_cop_billones: Optional[float] = Field(None, ge=0, description="Valor aproximado en COP billones")
    
    @validator('sector_economico')
    def clean_sector_name(cls, v):
        """Limpiar nombre del sector"""
        if not v or v.strip() == '':
            raise ValueError('El nombre del sector no puede estar vacío')
        return v.strip()
    
    @validator('participacion_porcentual')
    def validate_porcentaje(cls, v):
        """Validar que el porcentaje esté en rango válido"""
        if v < 0 or v > 100:
            raise ValueError(f'El porcentaje debe estar entre 0 y 100, recibido: {v}')
        return round(v, 2)
    
    @validator('valor_aproximado_cop_billones')
    def clean_valor_aproximado(cls, v):
        """Limpiar valor aproximado"""
        if v is None:
            return None
        if isinstance(v, str):
            # Limpiar texto y convertir a float
            v = re.sub(r'[^\d.,]', '', v)
            v = v.replace(',', '.')
            try:
                return float(v)
            except ValueError:
                return None
        return v
    
    class Config:
        """Configuración del modelo"""
        validate_assignment = True
        extra = "forbid"