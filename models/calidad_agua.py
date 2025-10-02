"""Modelo Pydantic para calidad del agua."""
from typing import Optional
from pydantic import Field, validator
from .base import BaseDataModel

class CalidadAguaModel(BaseDataModel):
    """Modelo para datos de calidad del agua."""
    año: int = Field(..., ge=2000, le=2030, description="Año")
    indice_riesgo_calidad_agua: Optional[float] = Field(None, ge=0, description="Índice de riesgo")
    municipios_sin_riesgo: Optional[int] = Field(None, ge=0, description="Municipios sin riesgo")
    municipios_riesgo_medio: Optional[int] = Field(None, ge=0, description="Municipios con riesgo medio")
    municipios_riesgo_alto: Optional[int] = Field(None, ge=0, description="Municipios con riesgo alto")
    
    @validator('año', pre=True)
    def validate_año(cls, v):
        if isinstance(v, str):
            return int(float(v.strip()))
        return int(v)
    
    @validator('indice_riesgo_calidad_agua', 'municipios_sin_riesgo', 'municipios_riesgo_medio', 'municipios_riesgo_alto', pre=True)
    def validate_numbers(cls, v):
        if v is None or v == '':
            return None
        try:
            return float(str(v).replace(',', '.'))
        except (ValueError, TypeError):
            return None
