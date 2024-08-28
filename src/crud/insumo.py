from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.models import Insumo

DETAILS_EXCEPTION = 'Insumo no encontrado'


def get_insumo_by_id(db, id: int):
    # res = db.query(UnidadMedida).filter(UnidadMedida.id_unidad_medida == unidad_id).first()
    res = db.query(Insumo).get(id)
    if res == None:
        raise HTTPException(
            status_code=201, detail=DETAILS_EXCEPTION)
    return res


def get_insumos(db):
    res=  db.query(Insumo).all()
    if len(res) != 0:
        return res
    raise HTTPException(
        status_code=201, detail="No hay listado")