from typing import Optional
from pydantic import BaseModel


class ClienteRequest(BaseModel):
    id_cliente: Optional[int] = None
    nombre_cliente: Optional[str] = None
    apellido_cliente: Optional[str] = None
    direccion_cliente: Optional[str] = None
    telefono_cliente: Optional[str] = None
    email_cliente: Optional[str] = None
