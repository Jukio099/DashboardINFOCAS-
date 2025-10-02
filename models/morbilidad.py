"""
Modelo Pydantic para validación de datos de morbilidad
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
import re

class Morbilidad(BaseModel):
    """Modelo para validar datos de morbilidad"""
    
    item: int = Field(..., ge=1, description="Número de item")
    sector: str = Field(..., description="Sector")
    programa: str = Field(..., description="Programa")
    tema: str = Field(..., description="Tema")
    subtema: str = Field(..., description="Subtema")
    dimension: str = Field(..., description="Dimensión")
    variables: str = Field(..., description="Variables")
    indicador: str = Field(..., description="Indicador")
    tipo_de_medida: str = Field(..., description="Tipo de medida")
    nivel_de_desagregacion: str = Field(..., description="Nivel de desagregación")
    año: int = Field(..., ge=2000, le=2030, description="Año")
    valor: int = Field(..., ge=0, description="Valor del indicador")
    estado: str = Field(..., description="Estado")
    año_de_creacion: int = Field(..., ge=0, description="Año de creación")
    año_de_baja: int = Field(..., ge=0, description="Año de baja")
    fuente_indicador: str = Field(..., description="Fuente del indicador")
    periodo_tiempo: str = Field(..., description="Período de tiempo")
    observaciones: Optional[str] = Field(None, description="Observaciones")
    
    @validator('indicador')
    def clean_indicador(cls, v):
        """Limpiar indicador"""
        if not v or v.strip() == '':
            raise ValueError('El indicador no puede estar vacío')
        return v.strip()
    
    @validator('valor')
    def validate_valor(cls, v):
        """Validar valor del indicador"""
        if v < 0:
            raise ValueError(f'El valor no puede ser negativo: {v}')
        return int(v)
    
    @validator('año')
    def validate_año(cls, v):
        """Validar año"""
        if v < 2000 or v > 2030:
            raise ValueError(f'El año debe estar entre 2000 y 2030, recibido: {v}')
        return int(v)
    
    class Config:
        """Configuración del modelo"""
        validate_assignment = True
        extra = "forbid"