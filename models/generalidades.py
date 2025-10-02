"""
Modelo Pydantic para validación de datos generales
"""

from pydantic import BaseModel, Field, validator
from typing import Optional

class Generalidades(BaseModel):
    """Modelo para validar datos generales"""
    
    pilar_competitividad: str = Field(..., description="Pilar de competitividad")
    indicador: str = Field(..., description="Indicador")
    año: int = Field(..., ge=2000, le=2030, description="Año")
    valor: float = Field(..., ge=0, description="Valor del indicador")
    unidad: str = Field(..., description="Unidad de medida")
    ranking_nacional: Optional[int] = Field(None, ge=1, le=50, description="Ranking nacional")
    fuente: str = Field(..., description="Fuente de datos")
    
    @validator('pilar_competitividad')
    def clean_pilar_competitividad(cls, v):
        """Limpiar pilar de competitividad"""
        if not v or v.strip() == '':
            raise ValueError('El pilar de competitividad no puede estar vacío')
        return v.strip()
    
    @validator('indicador')
    def clean_indicador(cls, v):
        """Limpiar indicador"""
        if not v or v.strip() == '':
            raise ValueError('El indicador no puede estar vacío')
        return v.strip()
    
    @validator('año')
    def validate_año(cls, v):
        """Validar año"""
        if v < 2000 or v > 2030:
            raise ValueError(f'El año debe estar entre 2000 y 2030, recibido: {v}')
        return int(v)
    
    @validator('valor')
    def validate_valor(cls, v):
        """Validar valor del indicador"""
        if v < 0:
            raise ValueError(f'El valor no puede ser negativo: {v}')
        return round(float(v), 2)
    
    @validator('unidad')
    def clean_unidad(cls, v):
        """Limpiar unidad de medida"""
        if not v or v.strip() == '':
            raise ValueError('La unidad no puede estar vacía')
        return v.strip()
    
    @validator('fuente')
    def clean_fuente(cls, v):
        """Limpiar fuente"""
        if not v or v.strip() == '':
            raise ValueError('La fuente no puede estar vacía')
        return v.strip()
    
    class Config:
        """Configuración del modelo"""
        validate_assignment = True
        extra = "forbid"