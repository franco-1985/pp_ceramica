from collections import defaultdict
from datetime import timedelta, datetime
import decimal
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.models import Pedido
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy.exc import NoResultFound
from src.crud.detallepedido import get_detalle_pedido_by_pedido
from src.crud.producto import get_insumos_producto, get_fases_producto


DETAILS_EXCEPTION = 'Pedido no encontrado'


def get_pedidos(db):
    res = db.query(Pedido).all()
    if not res:
        raise HTTPException(
            status_code=201, detail="No hay listados")
    return res


def get_pedido_by_id(db, id: int):
    res = db.query(Pedido).get(id)
    if not res:
        raise HTTPException(
            status_code=201, detail=DETAILS_EXCEPTION)
    return res


# def get_pedido_full_info(db: sessionmaker, id_pedido: int):
#     pedido_completo = {}
#     pedido_completo['pedido'] = get_pedido_by_id(db=db, id=id_pedido)
#     pedido_completo['detalle_pedido'] = get_detalle_pedido_by_pedido(
#         db=db, id_pedido=id_pedido)
#     total_sum = sum(item.total for item in pedido_completo['detalle_pedido'])
#     total_cant_producto = sum(
#         item.cantidad_producto for item in pedido_completo['detalle_pedido'])
#     pedido_completo['pedido'].total_pedido = total_sum
#     pedido_completo['pedido'].cantidad_productos_total = total_cant_producto
#     if pedido_completo['pedido'].fecha_entrega_aproximado == None:
#         update_fecha_entrega(db, pedido_completo)
#         # print(pedido_completo)
#     return pedido_completo


def get_insumos_pedido(db: sessionmaker, id_pedido: int):
    res = get_pedido_full_info(db=db, id_pedido=id_pedido)
    acumulado = defaultdict(lambda: {'cantidad_total': 0, 'precio_total': 0.0})
    total_insumos = defaultdict(lambda: 0.0)
    for item in res['detalle_pedido']:
        producto_id = item.id_producto
        # acumulado[producto_id]['nombre_producto'] = item.nombre_producto
        acumulado[producto_id]['cantidad_total'] += item.cantidad_producto
        acumulado[producto_id]['precio_total'] += float(item.total)
    resultado = []
    for producto_id, valores in acumulado.items():
        insumos = get_insumos_producto(db=db, id_producto=producto_id)
        detalle_insumo = []
        for item_insumo in insumos:
            total_insumo = item_insumo.cantidad * valores['cantidad_total']
            detalle_insumo.append({
                'insumo_id': item_insumo.id_insumo,
                'nombre_insumo': item_insumo.nombre_insumo,
                'total_insumo': total_insumo,
                'unidad_medida': item_insumo.nombre_unidad_medida
            })
            total_insumos[item_insumo.nombre_insumo] += float(total_insumo)
        resultado.append({
            'producto': producto_id,
            # 'nombre_producto': valores['nombre_producto'],
            'cantidad_total': valores['cantidad_total'],
            'precio_total': valores['precio_total'],
            'detalle_insumo': detalle_insumo
        })
    # Agregar la suma total de cada insumo al resultado
    resumen_insumos = []
    for nombre_insumo, total in total_insumos.items():
        resumen_insumos.append({
            'nombre_insumo': nombre_insumo,
            'total_acumulado': total
        })
    resultado.append({
        'resumen_insumos': resumen_insumos
    })
    return resultado


def get_pedido_full_info(db: sessionmaker, id_pedido: int):
    pedido_completo = {}
    # aca busco todos los datos del peiddo, pero a la vez traigo todos los datos del cliente. Previamente cree la relacion en el modelo
    pedido = db.query(Pedido).options(selectinload(Pedido.cliente)).filter(Pedido.id_pedido == id_pedido).one_or_none()

    # pedido_completo['pedido'] = get_pedido_by_id(db=db, id=id_pedido)
    pedido_completo['pedido'] = pedido


    pedido_completo['detalle_pedido'] = get_detalle_pedido_by_pedido(
        db=db, id_pedido=id_pedido)
    total_sum = sum(item.total for item in pedido_completo['detalle_pedido'])
    total_cant_producto = sum(
        item.cantidad_producto for item in pedido_completo['detalle_pedido'])
    pedido_completo['pedido'].total_pedido = total_sum
    pedido_completo['pedido'].cantidad_productos_total = total_cant_producto
    if pedido_completo['pedido'].fecha_entrega_aproximado == None:
        print('Pedido sin fecha de entrega aproximado')
    return pedido_completo



def update_fechas(db: sessionmaker, pedido: Pedido):
    # res_pedido = get_pedido_by_id(db=db, id=pedido.id_pedido)
    # msg = {'status': 0,
    #        'mensaje': f"Este pedido ya fue actualizado."}
    # if pedido.fecha_entrega_aproximado != None:
    res = update_fecha_entrega(db=db, id_pedido=pedido.id_pedido)
    if pedido.fecha_entrega_real != None:
        res = update_fecha_entrega_real(db=db, pedido=pedido)
    # msg = {'status': 0,
    #        'mensaje': f"Pedido con sus fechas actualizadas."}
    # return JSONResponse(content=msg, status_code=200)
    return res


def update_fecha_entrega(db: sessionmaker, id_pedido: int):
    res_detalle_pedido = get_detalle_pedido_by_pedido(
        db=db, id_pedido=id_pedido)
    res_pedido = get_pedido_by_id(db=db, id=id_pedido)
    msg = {'status': 0,
           'mensaje': f"Este pedido ya fue actualizado."}
    if res_pedido.fecha_entrega_aproximado == None:
        for i in res_detalle_pedido:
            list_dias = []
            res_fase = get_fases_producto(db=db, id_producto=i.id_producto)
            res_dias = res_fase['producto']['cantidad_dias']
            list_dias.append(res_dias)
        max_dias = max(list_dias)
        fecha_mas = res_pedido.fecha_pedido + timedelta(days=max_dias)
        if fecha_mas.weekday() > 5:
            print('entro un finde')
            fecha_mas += timedelta(2)
        res_pedido.fecha_entrega_aproximado = fecha_mas
        db.commit()
        db.expire_all()
        msg = {'status': 0,
               'mensaje': f"Se actualizo la fecha de entrega aproximada del pedido {id_pedido}."}
    print(msg)
    return JSONResponse(content=msg, status_code=200)


def update_fecha_entrega_real(db: sessionmaker, pedido: Pedido):
    res_pedido = get_pedido_by_id(db=db, id=pedido.id_pedido)
    msg = {'status': 0,
           'mensaje': f"Este pedido ya fue actualizado."}
    if res_pedido.fecha_entrega_real == None:
        print(f'Fecha de entrega real vacia {pedido.fecha_entrega_real}')
        res_pedido.fecha_entrega_real = pedido.fecha_entrega_real
        db.commit()
        db.expire_all()
        msg = {'status': 0,
               'mensaje': f"Se actualizo la fecha de entrega real del pedido {pedido.id_pedido}."}
    print(msg)
    return JSONResponse(content=msg, status_code=200)


def insert_pedido(db, pedido: Pedido):
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    msg = {'status': 0,
           'mensaje': f"Se inserto el pedido correctamente con el id {pedido}"}
    return JSONResponse(content=msg, status_code=200)


# def update_fecha(db: sessionmaker, nueva_fecha: dict):
#     try:
#         pedido = db.query(Pedido).filter(Pedido.id_pedido ==
#                                          nueva_fecha['pedido'].id_pedido).one()
#         # pedido = nueva_fecha['pedido']
#         pedido.fecha_entrega_aproximado = nueva_fecha['fecha']
#         db.commit()
#         db.refresh(pedido)
#         db.expire_all()
#     except NoResultFound:
#         print(f"No se encontró el pedido con id {
#               nueva_fecha['pedido'].id_pedido}")
#         db.rollback()
#         return None
#     except Exception as e:
#         print(f"Error al {
#               nueva_fecha['pedido'].id_pedido} actualizar el pedido: {str(e)}")
#         db.rollback()
#         return None
