from typing import Optional
from pydantic import BaseModel


class EstadoRequest(BaseModel):
    id_estado_pedido: Optional[int] = None
    nombre_estado: Optional[str] = None

