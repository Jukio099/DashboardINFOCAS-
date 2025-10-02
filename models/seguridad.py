"""
Modelo Pydantic para validación de datos de seguridad
"""

from pydantic import BaseModel, Field, validator
from typing import Optional

class Seguridad(BaseModel):
    """Modelo para validar datos de seguridad"""
    
    tipo_delito: str = Field(..., description="Tipo de delito")
    casos_2023: int = Field(..., ge=0, description="Casos en 2023")
    casos_2024: int = Field(..., ge=0, description="Casos en 2024")
    variacion_porcentual: float = Field(..., description="Variación porcentual")
    tendencia: str = Field(..., description="Tendencia")
    impacto: str = Field(..., description="Impacto")
    observaciones: Optional[str] = Field(None, description="Observaciones")
    
    @validator('tipo_delito')
    def clean_tipo_delito(cls, v):
        """Limpiar tipo de delito"""
        if not v or v.strip() == '':
            raise ValueError('El tipo de delito no puede estar vacío')
        return v.strip()
    
    @validator('casos_2023', 'casos_2024')
    def validate_casos(cls, v):
        """Validar número de casos"""
        if v < 0:
            raise ValueError(f'El número de casos no puede ser negativo: {v}')
        return int(v)
    
    @validator('variacion_porcentual')
    def validate_variacion(cls, v):
        """Validar variación porcentual"""
        return round(float(v), 2)
    
    @validator('tendencia')
    def clean_tendencia(cls, v):
        """Limpiar y validar tendencia"""
        if not v or v.strip() == '':
            raise ValueError('La tendencia no puede estar vacía')
        
        v = v.strip().lower()
        if 'aumento' in v or 'incremento' in v:
            return 'Aumento'
        elif 'disminución' in v or 'disminucion' in v or 'reducción' in v:
            return 'Disminución'
        elif 'estable' in v or 'constante' in v:
            return 'Estable'
        else:
            return v.title()
    
    @validator('impacto')
    def clean_impacto(cls, v):
        """Limpiar y validar impacto"""
        if not v or v.strip() == '':
            raise ValueError('El impacto no puede estar vacío')
        
        v = v.strip().lower()
        if 'alto' in v:
            return 'Alto'
        elif 'medio' in v or 'moderado' in v:
            return 'Medio'
        elif 'bajo' in v:
            return 'Bajo'
        else:
            return v.title()
    
    class Config:
        """Configuración del modelo"""
        validate_assignment = True
        extra = "forbid"