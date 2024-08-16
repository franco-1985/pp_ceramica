from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.schemas.tiempo import TiempoRequest


from src.crud.tiempo import get_tiempos, get_tiempo_by_id


tiempo = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@tiempo.get("/tiempo/", tags=["Tiempo"], response_model=list[TiempoRequest], name='Devolver listado de tiempos')
def get(db: Session = Depends(get_db)):
    try:
        return get_tiempos(db)
    except Exception as ex:
        msg = {'status': -1,
               "mensaje:": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)


@tiempo.get("/tiempo/{id}", tags=["Tiempo"], name='Devolver un tiempo')
def get_by_id(id: int, db: Session = Depends(get_db)):
    try:
        return get_tiempo_by_id(db, id)
    except Exception as ex:
        msg = {'status': -1,
               "mensaje:": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)
