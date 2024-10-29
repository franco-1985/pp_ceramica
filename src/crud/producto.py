import random
from sqlalchemy.orm import joinedload
from sqlalchemy.dialects import mysql
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.models import Producto, Productoxinsumo, Productoxfase, t_productoporfase, Insumo

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
        status_code=201, detail="No hay listadosss")


def get_insumos_producto(db, id_producto: int):
    res = db.query(Productoxinsumo).options(
        joinedload(Productoxinsumo.insumo),
        joinedload(Productoxinsumo.producto),
        joinedload(Productoxinsumo.unidad_medida)
    ).filter(Productoxinsumo.id_producto == id_producto).all()
    if not res:
        raise HTTPException(
            status_code=201, detail="No hay listado de productos"
        )
    res_res = []
    res_ins_prod = {}
    for res_prod_ins in res:
        print(f'{res_prod_ins.insumo.nombre_insumo}')
        res_prod_ins.nombre_insumo = res_prod_ins.insumo.nombre_insumo
        res_prod_ins.nombre_producto = res_prod_ins.producto.nombre_producto
        res_prod_ins.nombre_unidad_medida = res_prod_ins.unidad_medida.nombre_unidad_medida
        res_res.append(res_prod_ins)

    # res_ins_prod['producto'] = res_prod_ins.producto
    res_ins_prod['insumos'] = res_res
    return res


def get_fases_producto(db, id_producto: int):
    res_nom_prod = get_producto_by_id(db=db, id=id_producto)
    if res_nom_prod == None:
        res_nom_prod = 'todo mal papa'
    res_prod_fase = get_dias_producto_fases_x_nombre(
        db=db, nombre=res_nom_prod.nombre_producto)
    return {'producto': res_prod_fase}


def get_dias_producto_fases_x_nombre(db, nombre: str):
    res_producto = db.query(t_productoporfase).filter(
        t_productoporfase.c.nombre_producto == nombre).all()
    res_tiempo = 0
    for item in res_producto:
        res_tiempo += item[2]
    res_ponderador = random.randint(200, 250)
    res_cant_dias = round((res_ponderador * res_tiempo)/60/24)
    res = {}
    res['producto_fase'] = res_producto
    res['cantidad_dias'] = res_cant_dias
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
