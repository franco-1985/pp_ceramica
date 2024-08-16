# id_producto       = Column(INTEGER(11), primary_key=True)
# nombre_producto   = Column(String(100), nullable=False)
# precio_producto   = Column(Float(asdecimal=True))
# medida_producto   = Column(Float(asdecimal=True))
# id_unidad_medida  = Column(ForeignKey('unidad_medida.id_unidad_medida'), index=True)
# imagen            = Column(String(100))

from typing import Optional
from pydantic import BaseModel


class ProductoRequest(BaseModel):
    id_producto: Optional[int] = None
    nombre_producto: Optional[str] = None
    precio_producto: Optional[float] = None
    medida_producto: Optional[float] = None
    id_unidad_medida: Optional[float] = None
    imagen: Optional[str] = None
