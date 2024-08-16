from typing import Optional
from pydantic import BaseModel


class UnidadMedidaRequest(BaseModel):
    id_unidad_medida: Optional[int] = None
    nombre_unidad_medida: Optional[str] = None
    abreviatura_unidad_medida: Optional[str] = None