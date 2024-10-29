from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.models import DetallePedido, Producto
from src.crud.producto import get_producto_by_id
from src.crud.estado import get_estado_by_id


DETAILS_EXCEPTION = 'Detalle pedido no encontrado'


def get_detalles_pedidos(db):
    res = db.query(DetallePedido).all()
    print(res)
    if not res:
        raise HTTPException(
            status_code=201, detail="No hay listadoss")
    return res


def get_detalle_pedido_by_id(db, id: int):
    res = db.query(DetallePedido).filter(DetallePedido.id_detalle_pedido == id).all()
    print(len(res))
    if not res:
        raise HTTPException(
            status_code=201, detail=DETAILS_EXCEPTION)
    return res


def get_detalle_pedido_by_pedido(db, id_pedido: int):
    lista_detalle = db.query(DetallePedido).filter(
        DetallePedido.id_pedido == id_pedido).all()
    if not lista_detalle:
        raise HTTPException(
            status_code=201, detail=DETAILS_EXCEPTION)
    for item_detalle in lista_detalle:
        # if (item_detalle.total != 0 or item_detalle.total == None):
        res_producto = get_producto_by_id(
            db=db, id=item_detalle.id_producto)
        item_detalle.nombre_producto = res_producto.nombre_producto
        item_detalle_estado = get_estado_by_id(
            db=db, id=item_detalle.id_estado_pedido)
        item_detalle.nombre_estado_detalle = item_detalle_estado.nombre_estado
    return lista_detalle


def insert_detalle_pedido(db, detalle: DetallePedido):
    res_producto = get_producto_by_id(
        db=db, id=detalle.id_producto)
    total = detalle.cantidad_producto * res_producto.precio_producto
    detalle.total = total
    db.add(detalle)
    db.commit()
    db.refresh(detalle)
    msg = {'status': 0,
           'mensaje': f"Se inserto el pedido correctamente con el id {detalle}"}
    return JSONResponse(content=msg, status_code=200)
