from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.models import DetallePedido, Producto
from src.crud.producto import get_producto_by_id
from src.crud.estado import get_estado_by_id


DETAILS_EXCEPTION = 'Detalle pedido no encontrado'


def get_detalles_pedidos(db):
    res = db.query(DetallePedido).all()
    if len(res) != 0:
        return res
    raise HTTPException(
        status_code=201, detail="No hay listado")


def get_detalle_pedido_by_id(db, id: int):
    res = db.query(DetallePedido).get(id)
    if res == None:
        raise HTTPException(
            status_code=201, detail=DETAILS_EXCEPTION)
    return res


def get_detalle_pedido_by_pedido(db, id_pedido: int):
    lista_detalle = db.query(DetallePedido).filter(
        DetallePedido.id_pedido == id_pedido).all()
    for item_detalle in lista_detalle:
        if (item_detalle.total == None):
            res_producto = get_producto_by_id(
                db=db, id=item_detalle.id_producto)
            total = item_detalle.cantidad_producto * res_producto.precio_producto
            item_detalle.total = total
            item_detalle.nombre_producto = res_producto.nombre_producto
            item_detalle_estado = get_estado_by_id(db=db, id=item_detalle.id_estado_pedido)
            item_detalle.nombre_estado_detalle = item_detalle_estado.nombre_estado
    if lista_detalle == None:
        raise HTTPException(
            status_code=201, detail=DETAILS_EXCEPTION)
    return lista_detalle


def update_precio_producto_detalle(id_detalle_pedido: int):
    pass
