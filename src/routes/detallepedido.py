from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.models.models import DetallePedido
from src.schemas.detallepedido import DetallePedidoRequest
from src.crud.detallepedido import get_detalle_pedido_by_id, get_detalles_pedidos, insert_detalle_pedido


detpedido = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@detpedido.get("/detpedido/", tags=["Detalle de pedido"], response_model=list[DetallePedidoRequest], name='Devolver listado de detalle de pedido')
def get(db: Session = Depends(get_db)):
    try:
        return get_detalles_pedidos(db)
    except Exception as ex:
        msg = {'status': -1,
               "mensaje": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)


@detpedido.get("/detpedido/{id}", tags=["Detalle de pedido"], name='Devolver un detalle de pedido')
def get_by_id(id: int, db: Session = Depends(get_db)):
    try:
        return get_detalle_pedido_by_id(db, id)
    except Exception as ex:
        msg = {'status': -1,
               "mensaje": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)


@detpedido.post("/detpedido", tags=["Detalle de pedido"], name='Insertar detalle de pedido')
def post_detalle_pedido(detalle: DetallePedidoRequest, db: Session = Depends(get_db)):
    try:
        return insert_detalle_pedido(db=db, detalle=DetallePedido(**detalle.model_dump(exclude_unset=True)))
    except Exception as ex:
        msg = {'status': -1,
               "mensaje": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)
