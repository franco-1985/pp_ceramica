from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.models import DetallePedido


DETAILS_EXCEPTION = 'Detalle pedido no encontrado'


def get_detalles_pedidos(db):
    res = db.query(DetallePedido).all()
    if len(res) != 0:
        return res
    raise HTTPException(
        status_code=201, detail="No hay listado")


def get_detalle_pedido_by_id(db, id: int):
    # res = db.query(UnidadMedida).filter(UnidadMedida.id_unidad_medida == unidad_id).first()
    res = db.query(DetallePedido).get(id)
    if res == None:
        raise HTTPException(
            status_code=201, detail=DETAILS_EXCEPTION)
    return res
