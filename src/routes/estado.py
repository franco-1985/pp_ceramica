# from json import dumps
# from fastapi.responses import JSONResponse
# from src.db.db import conn

from fastapi.responses import JSONResponse
from src.db.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends  # , HTTPException
from src.crud.estado import get_estado_by_id, get_estados as get_estado

estado = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@estado.get("/estado", tags=["Estado"], name="Devolver listado de estados")
def get(db: Session = Depends(get_db)):
    try:
        return get_estado(db=db)
    except Exception as ex:
        msg = {'status': -1,
               "mensaje": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)


@estado.get("/estado/{id}", tags=["Estado"], name="Devolver un estado")
def get_by_id(id: int, db: Session = Depends(get_db)):
    try:
        return get_estado_by_id(db=db, id=id)
    except Exception as ex:
        msg = {'status': -1,
               "mensaje": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)

    # sql = "select * from estado where id_estado={0}".format(id)
    # return __traer_estado(sql=sql)


# def __traer_estado(sql: str):
#     try:
#         res_cursor = conn.cursor()
#         print(f'----->query del select por id -> {sql}')
#         res_cursor.execute(sql)
#         estado = res_cursor.fetchall()
#         estados = []
#         if (len(estado) == 0):
#             raise HTTPException(
#                 status_code=200, detail='Estado no encontrado')
#         else:
#             for res_est in estado:
#                 res = {}
#                 res["id_estado"] = res_est[0]
#                 res["nombre_estado"] = res_est[1]
#                 estados.append(res)
#         msg = {'status': 0, 'mensaje': estados}
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
