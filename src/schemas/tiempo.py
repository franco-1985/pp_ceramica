from typing import Optional
from pydantic import BaseModel


class TiempoRequest(BaseModel):

    id_tiempo: Optional[int] = None
    cantidad_tiempo: Optional[int] = None
    id_unidad_medida: Optional[int] = None
