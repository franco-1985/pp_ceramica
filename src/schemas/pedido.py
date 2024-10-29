from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class PedidoRequest(BaseModel):
    id_pedido: Optional[int] = None
    fecha_pedido: Optional[datetime] = None
    fecha_entrega_aproximado: Optional[datetime] = None
    fecha_entrega_real: Optional[datetime] = None
    id_estado_pedido: Optional[int] = 3
    id_cliente: Optional[int] = None
    # id_detalle_pedido: Optional[int] = None

class UpdatePedidoFechasRequest(BaseModel):
    id_pedido: Optional[int] = None
    # fecha_entrega_aproximado: Optional[datetime] = None
    fecha_entrega_real: Optional[datetime] = None
