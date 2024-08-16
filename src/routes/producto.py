from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.schemas.producto import ProductoRequest


from src.crud.producto import get_productos, get_producto_by_id


producto = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@producto.get("/producto/", tags=["Producto"], response_model=list[ProductoRequest],name='Devolver listado de productos')
def get(db: Session = Depends(get_db)):
    try:
        return get_productos(db)
    except Exception as ex:
        msg = {'status': -1,
            "mensaje:": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)


@producto.get("/producto/{id}", tags=["Producto"], name='Devolver un producto')
def get_by_id(id: int, db: Session = Depends(get_db)):
    try:
        return get_producto_by_id(db, id)
    except Exception as ex:
        msg = {'status': -1,
            "mensaje:": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)
