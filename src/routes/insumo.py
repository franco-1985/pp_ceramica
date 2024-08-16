from json import dumps
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.db.database import SessionLocal
from sqlalchemy.orm import Session
# from src.db.db import conn
from src.crud.insumo import get_insumos as get_insumo, get_insumo_by_id

insumo = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@insumo.get("/insumo", tags=["Insumo"], name="Devolver listado de insumos")
def get(db: Session = Depends(get_db)):
    try:
        return get_insumo(db)
    except Exception as ex:
        msg = {'status': -1,
               "mensaje:": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)


@insumo.get("/insumo/{id}", tags=["Insumo"], name="Devolver un insumo")
def get(id: int, db: Session = Depends(get_db)):
    try:
        return get_insumo_by_id(db, id)
    except Exception as ex:
        msg = {'status': -1,
               "mensaje:": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)


# def get_insumo(id: int):
#     sql = "select * from insumo where id_insumo={0}".format(id)
#     return __traer_insumo(sql=sql)


# def __traer_insumo(sql: str):
#     try:
#         res_cursor = conn.cursor()
#         print(f'----->query del select por id -> {sql}')
#         res_cursor.execute(sql)
#         insumo = res_cursor.fetchall()
#         insumos = []
#         if (len(insumo) == 0):
#             raise HTTPException(
#                 status_code=200, detail='Insumo no encontrado')
#         else:
#             for res_ins in insumo:
#                 res = {}
#                 res["id_fase"] = res_ins[0]
#                 res["nombre_fase"] = res_ins[1]
#                 insumos.append(res)
#         msg = {'status': 0, 'mensaje': insumos}
#         return JSONResponse(content=msg)
#     except HTTPException as ex:
#         msg = {'status': -1,
#                "mensaje:": ex.detail}
#         return JSONResponse(content=msg, status_code=ex.status_code)
#     except Exception as ex:
#         msg = {'status': -1,
#                "mensaje:": ex.detail}
#         return JSONResponse(content=ex.detail, status_code=ex.status_code)
#     finally:
#         res_cursor.close()
