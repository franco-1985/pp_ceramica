from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.models import Producto

DETAILS_EXCEPTION = 'Producto no encontrado'


def get_producto_by_id(db, id: int):
    # res = db.query(UnidadMedida).filter(UnidadMedida.id_unidad_medida == unidad_id).first()
    res = db.query(Producto).get(id)
    if res == None:
        raise HTTPException(
            status_code=201, detail=DETAILS_EXCEPTION)
    return res


def get_productos(db):
    res = db.query(Producto).all()
    if len(res) != 0:
        return res
    raise HTTPException(
        status_code=201, detail="No hay listado")
