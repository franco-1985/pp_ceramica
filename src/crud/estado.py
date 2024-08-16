from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.models import Estado

DETAILS_EXCEPTION = 'Estado no encontrado'


def get_estado_by_id(db, id: int):
    # res = db.query(UnidadMedida).filter(UnidadMedida.id_unidad_medida == unidad_id).first()
    res = db.query(Estado).get(id)
    if res == None:
        raise HTTPException(
            status_code=201, detail=DETAILS_EXCEPTION)
    return res


def get_estados(db):
    res = db.query(Estado).all()
    if len(res) != 0:
        return res
    raise HTTPException(
        status_code=201, detail="No hay listado")
