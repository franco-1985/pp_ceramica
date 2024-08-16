from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.models import UnidadMedida


DETAILS_EXCEPTION = 'Unidad de medida no encontrada'


def get_unidades_medida(db):
    res =  db.query(UnidadMedida).all()
    if len(res) != 0:
        return res
    raise HTTPException(
        status_code=201, detail="No hay listado")


def get_unidades_medidas_by_id(db, id: int):
    # res = db.query(UnidadMedida).filter(UnidadMedida.id_unidad_medida == unidad_id).first()
    res = db.query(UnidadMedida).get(id)
    if res == None:
        raise HTTPException(
            status_code=201, detail=DETAILS_EXCEPTION)
    return res