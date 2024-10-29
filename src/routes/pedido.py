from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.models.models import Pedido
from src.schemas.pedido import PedidoRequest, UpdatePedidoFechasRequest
from src.crud.pedido import get_pedido_by_id, get_pedidos, get_pedido_full_info, insert_pedido, update_fecha_entrega, update_fechas


pedido = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pedido.get("/pedido/", tags=["Pedido"], response_model=list[PedidoRequest], name='Devolver listado de pedidos')
def get(db: Session = Depends(get_db)):
    try:
        return get_pedidos(db)
    except Exception as ex:
        msg = {'status': -1,
               "mensaje": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)


@pedido.get("/pedido/{id}", tags=["Pedido"], name='Devolver un pedido')
def get_by_id(id: int, db: Session = Depends(get_db)):
    try:
        return get_pedido_by_id(db, id)
    except Exception as ex:
        msg = {'status': -1,
               "mensaje": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)


@pedido.get("/pedido_detalle/{id}", tags=["Pedido"], name='Devolver un pedido completo')
def get_pedido_detalle_by(id: int, db: Session = Depends(get_db)):
    try:
        return get_pedido_full_info(id_pedido=id, db=db)
    except Exception as ex:
        msg = {'status': -1,
               "mensaje": str(ex.detail)}
        # "mensaje": str(ex)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)


@pedido.put("/pedido", tags=["Pedido"], name='Actualizar fecha de pedido')
def update_data_delivery_aprox_by_id(pedido: UpdatePedidoFechasRequest, db: Session = Depends(get_db)):
    try:
        return update_fechas(db=db, pedido=pedido)
    except Exception as ex:
        msg = {'status': -1,
               "mensaje": str(ex.detail)}
        # "mensaje": str(ex)}
        status = ex.status_code
    return JSONResponse(content=msg, status_code=status)


@pedido.post("/pedido", tags=["Pedido"], name='Insertar nuevo pedido')
def post_pedido(pedido: PedidoRequest, db: Session = Depends(get_db)):
    try:
        pedido.id_pedido = None
        pedido.fecha_entrega_aproximado = None
        pedido.fecha_entrega_real = None
        return insert_pedido(db=db, pedido=Pedido(**pedido.model_dump(exclude_unset=True)))
    except Exception as ex:
        msg = {'status': -1,
               "mensaje": str(ex.detail)}
        # "mensaje": str(ex)}
        status = ex.status_code
    return JSONResponse(content=msg, status_code=status)
