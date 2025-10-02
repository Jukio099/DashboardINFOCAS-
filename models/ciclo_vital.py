"""
Modelo Pydantic para datos de ciclo vital demográfico.
"""

from typing import Optional
from pydantic import Field, validator
from .base import BaseDataModel


class CicloVitalModel(BaseDataModel):
    """Modelo para datos de ciclo vital demográfico."""
    
    ciclo_vital: str = Field(..., description="Etapa del ciclo vital")
    poblacion: Optional[float] = Field(None, ge=0, description="Población en la etapa")
    peso_relativo: Optional[float] = Field(
        None, 
        ge=0, 
        le=1, 
        description="Peso relativo (proporción)"
    )
    
    @validator('poblacion', pre=True)
    def validate_poblacion(cls, v):
        """Valida y limpia la población."""
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
    
    @validator('peso_relativo', pre=True)
    def validate_peso_relativo(cls, v):
        """Valida y limpia el peso relativo."""
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
    
    @validator('ciclo_vital')
    def validate_ciclo_vital(cls, v):
        """Valida y normaliza el ciclo vital."""
        if not v or v.strip() == '':
            raise ValueError("Ciclo vital es requerido")
        
        # Normalizar nombres de etapas
        ciclo = v.strip()
        ciclo_lower = ciclo.lower()
        
        if 'primera infancia' in ciclo_lower or '0-5' in ciclo:
            return 'Primera infancia 0-5 años'
        elif 'infancia' in ciclo_lower and '6-11' in ciclo:
            return 'Infancia 6-11 años'
        elif 'adolescencia' in ciclo_lower or '12-17' in ciclo or '12-18' in ciclo:
            return 'Adolescencia 12-17 años'
        elif 'juventud' in ciclo_lower or '18-28' in ciclo or '19-28' in ciclo:
            return 'Juventud 18-28 años'
        elif 'adultez' in ciclo_lower or '29-59' in ciclo:
            return 'Adultez 29-59 años'
        elif 'mayor' in ciclo_lower or '60' in ciclo:
            return 'Persona mayor 60 años y más'
        elif 'total' in ciclo_lower:
            return 'Total'
        else:
            return ciclo
    
    class Config:
        """Configuración específica del modelo."""
        schema_extra = {
            "example": {
                "ciclo_vital": "Primera infancia 0-5 años",
                "poblacion": 45024.0,
                "peso_relativo": 0.09342280542310422
            }
        }
