from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.models import Pedido


DETAILS_EXCEPTION = 'Pedido no encontrado'


def get_pedidos(db):
    res = db.query(Pedido).all()
    if len(res) != 0:
        return res
    raise HTTPException(
        status_code=201, detail="No hay listado")


def get_pedido_by_id(db, id: int):
    res = db.query(Pedido).get(id)
    if res == None:
        raise HTTPException(
            status_code=201, detail=DETAILS_EXCEPTION)
    return res
