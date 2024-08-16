from typing import Optional
from pydantic import BaseModel
from datetime import date


class PedidoRequest(BaseModel):
    id_pedido: Optional[int] = None
    fecha_pedido: Optional[date] = None
    fecha_entrega_aproximado: Optional[date] = None
    fecha_entrega_real: Optional[date] = None
    id_estado_pedido: Optional[int] = None
    id_cliente: Optional[int] = None
    id_detalle_pedido: Optional[int] = None
