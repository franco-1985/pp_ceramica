from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.models import Cliente


DETAILS_EXCEPTION = 'Cliente no encontrado'


def get_clientes(db):
    res = db.query(Cliente).all()
    if len(res) != 0:
        return res
    raise HTTPException(
        status_code=201, detail="No hay listado")


def get_cliente_by_id(db, id: int):
    res = db.query(Cliente).get(id)
    if res == None:
        raise HTTPException(
            status_code=201, detail=DETAILS_EXCEPTION)
    return res
