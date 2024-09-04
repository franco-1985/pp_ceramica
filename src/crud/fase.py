from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.models import Fase

DETAILS_EXCEPTION = 'Fase no encontrada'


def get_fase_by_id(db, id: int):
    # res = db.query(UnidadMedida).filter(UnidadMedida.id_unidad_medida == unidad_id).first()
    res = db.query(Fase).get(id)
    if res == None:
        raise HTTPException(
            status_code=201, detail=DETAILS_EXCEPTION)
    return res


def get_fases(db):
    res = db.query(Fase).all()
    if len(res) != 0:
        return res
    raise HTTPException(
        status_code=201, detail="No hay listado de fases")
