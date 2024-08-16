from typing import Optional
from pydantic import BaseModel


class InsumoRequest(BaseModel):
    id_insumo: Optional[int] = None
    nombre_insumo: Optional[str] = None