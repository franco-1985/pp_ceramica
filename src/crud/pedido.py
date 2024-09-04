from collections import defaultdict
import decimal
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.models import Pedido
from sqlalchemy.orm import sessionmaker
from src.crud.detallepedido import get_detalle_pedido_by_pedido
from src.crud.producto import get_insumos_productos


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


def get_pedido_full_info(db: sessionmaker, id_pedido: int):
    pedido_completo = {}
    pedido_completo['pedido'] = get_pedido_by_id(db=db, id=id_pedido)
    pedido_completo['detalle_pedido'] = get_detalle_pedido_by_pedido(
        db=db, id_pedido=id_pedido)
    total_sum = sum(item.total for item in pedido_completo['detalle_pedido'])
    total_cant_producto = sum(
        item.cantidad_producto for item in pedido_completo['detalle_pedido'])
    pedido_completo['pedido'].total_pedido = total_sum
    pedido_completo['pedido'].cantidad_productos_total = total_cant_producto
    return pedido_completo


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
        insumos = get_insumos_productos(db=db, id_producto=producto_id)

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

