from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.schemas.unidadmedida import UnidadMedidaRequest


from src.crud.unidadmedida import get_unidades_medida, get_unidades_medidas_by_id as get_unidad_medida_by_id


medida = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@medida.get("/unimedida/", tags=["Unidad de medida"], response_model=list[UnidadMedidaRequest], name='Devolver listado de unidad de medida')
def get(db: Session = Depends(get_db)):
    try:
        return get_unidades_medida(db)
    except Exception as ex:
        msg = {'status': -1,
               "mensaje:": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)


@medida.get("/unimedida/{id}", tags=["Unidad de medida"], name='Devolver una unidad de medida')
def get_by_id(id: int, db: Session = Depends(get_db)):
    try:
        return get_unidad_medida_by_id(db, id)
    except Exception as ex:
        msg = {'status': -1,
               "mensaje:": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)
