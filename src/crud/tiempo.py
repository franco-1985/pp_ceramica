from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.models import Tiempo


DETAILS_EXCEPTION = 'Tiempo no encontrado'


def get_tiempos(db):
    res = db.query(Tiempo).all()
    if len(res) != 0:
        return res
    raise HTTPException(
        status_code=201, detail="No hay listado de tiempos")


def get_tiempo_by_id(db, id: int):
    res = db.query(Tiempo).get(id)
    if res == None:
        raise HTTPException(
            status_code=201, detail=DETAILS_EXCEPTION)
    return res
