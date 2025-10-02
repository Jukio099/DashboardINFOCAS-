"""
Modelo Pydantic para validación de datos de graduados
"""

from pydantic import BaseModel, Field, validator
from typing import Optional

class Graduados(BaseModel):
    """Modelo para validar datos de graduados"""
    
    area_de_conocimiento: str = Field(..., description="Área de conocimiento")
    numero_de_graduados: int = Field(..., ge=0, description="Número de graduados")
    porcentaje_del_total: float = Field(..., ge=0, le=100, description="Porcentaje del total")
    
    @validator('area_de_conocimiento')
    def clean_area_conocimiento(cls, v):
        """Limpiar y validar área de conocimiento"""
        if not v or v.strip() == '':
            raise ValueError('El área de conocimiento no puede estar vacío')
        return v.strip()
    
    @validator('numero_de_graduados')
    def validate_numero_graduados(cls, v):
        """Validar número de graduados"""
        if v < 0:
            raise ValueError(f'El número de graduados no puede ser negativo: {v}')
        return int(v)
    
    @validator('porcentaje_del_total')
    def validate_porcentaje(cls, v):
        """Validar porcentaje del total"""
        if v < 0 or v > 100:
            raise ValueError(f'El porcentaje debe estar entre 0 y 100, recibido: {v}')
        return round(v, 2)
    
    class Config:
        """Configuración del modelo"""
        validate_assignment = True
        extra = "forbid"