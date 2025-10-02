"""
Modelo Pydantic para validación de datos empresariales
"""

from pydantic import BaseModel, Field, validator
from typing import Optional

class Empresarial(BaseModel):
    """Modelo para validar datos empresariales"""
    
    tamano_de_empresa: str = Field(..., description="Tamaño de la empresa")
    numero_de_empresas: int = Field(..., ge=0, description="Número de empresas")
    porcentaje_del_total: float = Field(..., ge=0, le=100, description="Porcentaje del total")
    
    @validator('tamano_de_empresa')
    def clean_tamano_empresa(cls, v):
        """Limpiar y validar tamaño de empresa"""
        if not v or v.strip() == '':
            raise ValueError('El tamaño de empresa no puede estar vacío')
        
        # Estandarizar nombres
        v = v.strip().lower()
        if 'micro' in v:
            return 'Micro'
        elif 'pequeña' in v or 'pequeña' in v:
            return 'Pequeña'
        elif 'mediana' in v:
            return 'Mediana'
        elif 'grande' in v:
            return 'Grande'
        else:
            return v.title()
    
    @validator('numero_de_empresas')
    def validate_numero_empresas(cls, v):
        """Validar número de empresas"""
        if v < 0:
            raise ValueError(f'El número de empresas no puede ser negativo: {v}')
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