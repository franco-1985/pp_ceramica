from typing import Optional
from pydantic import BaseModel


class DetallePedidoRequest(BaseModel):
    id_detalle_pedido: Optional[int] = None
    id_pedido: Optional[int] = None
    cantidad_producto: Optional[int] = None
    total: Optional[float] = None
    id_producto: Optional[int] = None
    id_estado_pedido: Optional[int] = None
