from typing import Optional
from pydantic import BaseModel


class FaseRequest(BaseModel):
    id_fase: Optional[int] = None
    nombre_fase: Optional[str] = None