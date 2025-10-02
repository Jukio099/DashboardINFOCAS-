"""
Modelos Pydantic para validación de datos del Dashboard de Casanare
"""

from .sector_economico import SectorEconomico
from .empresarial import Empresarial
from .graduados import Graduados
from .morbilidad import Morbilidad
from .seguridad import Seguridad
from .desercion import Desercion
from .generalidades import Generalidades

__all__ = [
    'SectorEconomico',
    'Empresarial', 
    'Graduados',
    'Morbilidad',
    'Seguridad',
    'Desercion',
    'Generalidades'
]