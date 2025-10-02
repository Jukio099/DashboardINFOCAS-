"""
Modelo Pydantic para validación de datos de deserción
"""

from pydantic import BaseModel, Field, validator
from typing import Optional

class Desercion(BaseModel):
    """Modelo para validar datos de deserción"""
    
    municipio: str = Field(..., description="Municipio")
    año: int = Field(..., ge=2000, le=2030, description="Año")
    tasa_desercion: float = Field(..., ge=0, le=1, description="Tasa de deserción (0-1)")
    sector: str = Field(..., description="Sector")
    observaciones: Optional[str] = Field(None, description="Observaciones")
    
    @validator('municipio')
    def clean_municipio(cls, v):
        """Limpiar nombre del municipio"""
        if not v or v.strip() == '':
            raise ValueError('El municipio no puede estar vacío')
        return v.strip().title()
    
    @validator('año')
    def validate_año(cls, v):
        """Validar año"""
        if v < 2000 or v > 2030:
            raise ValueError(f'El año debe estar entre 2000 y 2030, recibido: {v}')
        return int(v)
    
    @validator('tasa_desercion')
    def validate_tasa_desercion(cls, v):
        """Validar tasa de deserción"""
        if v < 0 or v > 1:
            raise ValueError(f'La tasa de deserción debe estar entre 0 y 1, recibido: {v}')
        return round(float(v), 4)
    
    @validator('sector')
    def clean_sector(cls, v):
        """Limpiar sector"""
        if not v or v.strip() == '':
            raise ValueError('El sector no puede estar vacío')
        return v.strip()
    
    class Config:
        """Configuración del modelo"""
        validate_assignment = True
        extra = "forbid"