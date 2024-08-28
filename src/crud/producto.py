from sqlalchemy.dialects import mysql
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.models import Producto, Productoxinsumo
from src.crud.insumo import get_insumo_by_id
from src.crud.unidadmedida import get_unidades_medidas_by_id

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


from sqlalchemy.orm import joinedload

def get_insumos_productos(db, id_producto: int):
    res = db.query(Productoxinsumo).options(
        joinedload(Productoxinsumo.insumo),
        joinedload(Productoxinsumo.producto),
        joinedload(Productoxinsumo.unidad_medida)
    ).filter(Productoxinsumo.id_producto == id_producto).all()

    if not res:
        raise HTTPException(
            status_code=201, detail="No hay listado"
        )

    for res_prod_ins in res:
        res_prod_ins.nombre_insumo = res_prod_ins.insumo.nombre_insumo
        res_prod_ins.nombre_producto = res_prod_ins.producto.nombre_producto
        res_prod_ins.nombre_unidad_medida = res_prod_ins.unidad_medida.nombre_unidad_medida

    return res


# def get_insumos_productos(db, id_producto: int):
#     res = db.query(Productoxinsumo).filter(
#         Productoxinsumo.id_producto == id_producto).all()
#     if len(res) != 0:
#         for res_prod_ins in res:
#             res_insumo = get_insumo_by_id(db=db, id=res_prod_ins.id_insumo).nombre_insumo
#             res_producto = get_producto_by_id(db=db, id=res_prod_ins.id_producto).nombre_producto
#             res_unidad_medida = get_unidades_medidas_by_id(db=db, id=res_prod_ins.id_unidad_medida).nombre_unidad_medida
#             res_prod_ins.nombre_insumo = res_insumo
#             res_prod_ins.nombre_producto = res_producto
#             res_prod_ins.nombre_unidad_medida = res_unidad_medida
#         return res
#     raise HTTPException(
#         status_code=201, detail="No hay listado")

