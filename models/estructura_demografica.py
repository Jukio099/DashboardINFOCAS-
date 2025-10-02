"""Modelo Pydantic para estructura demográfica."""
from typing import Optional
from pydantic import Field, validator
from .base import BaseDataModel

class EstructuraDemograficaModel(BaseDataModel):
    """Modelo para estructura demográfica."""
    indicador: str = Field(..., description="Indicador demográfico")
    valor: Optional[float] = Field(None, description="Valor del indicador")
    
    @validator('valor', pre=True)
    def validate_valor(cls, v):
        if v is None or v == '':
            return None
        try:
            return float(str(v).replace(',', '.'))
        except (ValueError, TypeError):
            return None
    
    @validator('indicador')
    def validate_indicador(cls, v):
        if not v or v.strip() == '':
            raise ValueError("Indicador es requerido")
        return v.strip()
