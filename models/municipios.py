"""
Modelo Pydantic para datos de municipios.
"""

from typing import Optional
from pydantic import Field, validator
from .base import BaseDataModel


class MunicipiosModel(BaseDataModel):
    """Modelo para datos de municipios."""
    
    municipio: str = Field(..., description="Nombre del municipio")
    numero_de_empresas: Optional[float] = Field(None, ge=0, description="Número de empresas")
    porcentaje_del_total: Optional[float] = Field(
        None, 
        ge=0, 
        le=100, 
        description="Porcentaje del total"
    )
    
    @validator('numero_de_empresas', pre=True)
    def validate_numero_empresas(cls, v):
        """Valida y limpia el número de empresas."""
        if v is None or v == '':
            return None
        
        try:
            if isinstance(v, str):
                cleaned = v.replace(',', '.').strip()
                if cleaned in ['', 'N/A', 'n/a']:
                    return None
                return float(cleaned)
            return float(v)
        except (ValueError, TypeError):
            return None
    
    @validator('porcentaje_del_total', pre=True)
    def validate_porcentaje(cls, v):
        """Valida y limpia el porcentaje."""
        if v is None or v == '':
            return None
        
        try:
            if isinstance(v, str):
                cleaned = v.replace(',', '.').strip()
                if cleaned in ['', 'N/A', 'n/a']:
                    return None
                return float(cleaned)
            return float(v)
        except (ValueError, TypeError):
            return None
    
    @validator('municipio')
    def validate_municipio(cls, v):
        """Valida el nombre del municipio."""
        if not v or v.strip() == '':
            raise ValueError("Nombre del municipio es requerido")
        return v.strip().title()  # Capitalizar correctamente
    
    class Config:
        """Configuración específica del modelo."""
        schema_extra = {
            "example": {
                "municipio": "Yopal",
                "numero_de_empresas": 12097.0,
                "porcentaje_del_total": 51.0
            }
        }
