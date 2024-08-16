from json import dumps
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.db.database import SessionLocal
# from src.db.db import conn
from sqlalchemy.orm import Session
from src.crud.fase import get_fases as get_fase, get_fase_by_id

fase = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@fase.get("/fase", tags=["Fase"], name="Devolver listado de fases")
def get(db: Session = Depends(get_db)):
    try:
        return get_fase(db=db)
    except Exception as ex:
        msg = {'status': -1,
            "mensaje:": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)

@fase.get("/fase/{id}", tags=["Fase"], name="Devolver una fase")
def get_by_id(id: int, db: Session = Depends(get_db)):
    try:
        return get_fase_by_id(db=db, id=id)
    except Exception as ex:
        msg = {'status': -1,
            "mensaje:": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)




# def get_estado(id: int):
#     sql = "select * from fase where id_fase={0}".format(id)
#     return __traer_fase(sql=sql)


# def __traer_fase(sql: str):
#     try:
#         res_cursor = conn.cursor()
#         print(f'----->query del select por id -> {sql}')
#         res_cursor.execute(sql)
#         fase = res_cursor.fetchall()
#         fases = []
#         if (len(fase) == 0):
#             raise HTTPException(
#                 status_code=200, detail='Fase no encontrado')
#         else:
#             for res_fas in fase:
#                 res = {}
#                 res["id_fase"] = res_fas[0]
#                 res["nombre_fase"] = res_fas[1]
#                 fases.append(res)
#         msg = {'status': 0, 'mensaje': fases}
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