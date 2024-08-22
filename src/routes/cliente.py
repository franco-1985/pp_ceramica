from json import dumps
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.db.database import SessionLocal
from src.db.db import conn
from sqlalchemy.orm import Session
from src.schemas.cliente import ClienteRequest
from src.models.models import Cliente
from src.crud.cliente import select_clientes, select_cliente_by_id, insert_cliente, update_cliente

cliente = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@cliente.get("/cliente", response_model=list[ClienteRequest], tags=["Cliente"], name="Devoler listado de clientes")
def get(db: Session = Depends(get_db)):
    try:
        return select_clientes(db=db)
    except Exception as ex:
        msg = {'status': -1,
               "mensaje": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)


@cliente.get("/cliente/{id}", tags=["Cliente"], name="Devolver un cliente")
def get_by_id(id: int, db: Session = Depends(get_db)):
    try:
        return select_cliente_by_id(db=db, id=id)
    except Exception as ex:
        msg = {'status': -1,
               "mensaje": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)


@cliente.post("/cliente", tags=["Cliente"], name="Agregar cliente")
def post_cliente(cliente: ClienteRequest, db: Session = Depends(get_db)):
    try:
        return insert_cliente(db=db, cliente=Cliente(**cliente.model_dump(exclude_unset=True)))
    except Exception as ex:
        msg = {'status': -1,
               "mensaje": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)


@cliente.put("/cliente", tags=["Cliente"], name="Actualizar cliente")
def put_cliente(cliente: ClienteRequest, db: Session = Depends(get_db)):
    try:
        if cliente.id_cliente != None:
            campos = {'id_cliente': cliente.id_cliente}
            if cliente.nombre_cliente is not None:
                campos['nombre_cliente'] = cliente.nombre_cliente
            if cliente.apellido_cliente is not None:
                campos['apellido_cliente'] = cliente.apellido_cliente
            if cliente.direccion_cliente is not None:
                campos['direccion_cliente'] = cliente.direccion_cliente
            if cliente.telefono_cliente is not None:
                campos['telefono_cliente'] = cliente.telefono_cliente
            if cliente.email_cliente is not None:
                campos['email_cliente'] = cliente.email_cliente
            return update_cliente(db=db, nuevos_datos=campos)
        else:
            msg = {'status': -1,
                "mensaje": 'Debe indicar un id al cual desea modificar al menos'}
            status = 400
            return JSONResponse(content=msg, status_code=status)
    except Exception as ex:
        msg = {'status': -1,
               "mensaje": str(ex.detail)}
        status = ex.status_code
        return JSONResponse(content=msg, status_code=status)

    # def get_cliente(id: int):
    #     sql = "select * from cliente where id_cliente={0}".format(id)
    #     return __traer_clientes(sql=sql)

    # def get_cliente():
    #     sql = "select * from cliente"
    #     return __traer_clientes(sql=sql, band=False)


# def __traer_clientes(sql: str, band: bool = True):
#     try:
#         res_cursor = conn.cursor()
#         print(f'----->query del select por id -> {sql}')
#         res_cursor.execute(sql)
#         cliente = res_cursor.fetchall()
#         clientes = []
#         if (len(cliente) == 0):
#             if band:
#                 raise HTTPException(
#                     status_code=200, detail='Cliente no encontrado')
#             else:
#                 msg = {'status': 0, 'mensaje': clientes}
#                 raise HTTPException(
#                     status_code=200, detail=msg)
#         else:
#             for res_cli in cliente:
#                 res = {}
#                 if res_cli[0] is not None:
#                     res["id_cliente"] = res_cli[0]
#                 if res_cli[1] is not None:
#                     res["nombre_cliente"] = res_cli[1]
#                 if res_cli[2] is not None:
#                     res["apellido_cliente"] = res_cli[2]
#                 if res_cli[3] is not None:
#                     res["direccion_cliente"] = res_cli[3]
#                 if res_cli[4] is not None:
#                     res["telefono_cliente"] = res_cli[4]
#                 if res_cli[5] is not None:
#                     res["email_cliente"] = res_cli[5]
#                 clientes.append(res)
#         msg = {'status': 0, 'mensaje': clientes}
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
#         print('---->close del cursor<----')
#         res_cursor.close()


# # @cliente.post("/cliente", tags=["Cliente"], name="Agregar cliente")
# def post_cliente(request: ClienteRequest):
#     try:
#         res_cursor = conn.cursor()
#         if request.id_cliente is not None:
#             sql = "select * from cliente where id_cliente= {0}".format(
#                 request.id_cliente)
#             print(f'----->query del select en el insert -> {sql}')
#             res_cursor.execute(sql)
#             cliente = res_cursor.fetchone()

#             if cliente:
#                 msg = {
#                     'status': -1, 'mensaje': "El cliente {0} ya existe en el sistema".format(request.id_cliente)}
#         else:
#             campos_insert = []
#             if request.id_cliente is not None:
#                 campos_insert.append(f"id_cliente = '{request.id_cliente}'")
#             if request.nombre_cliente is not None:
#                 campos_insert.append(f"nombre_cliente = '{
#                                      request.nombre_cliente}'")
#             if request.apellido_cliente is not None:
#                 campos_insert.append(f"apellido_cliente = '{
#                                      request.apellido_cliente}'")
#             if request.direccion_cliente is not None:
#                 campos_insert.append(f"direccion_cliente = '{
#                                      request.direccion_cliente}'")
#             if request.telefono_cliente is not None:
#                 campos_insert.append(f"telefono_cliente = '{
#                                      request.telefono_cliente}'")
#             if request.email_cliente is not None:
#                 campos_insert.append(f"email_cliente = '{
#                                      request.email_cliente}'")
#             if not campos_insert:
#                 raise HTTPException(
#                     status_code=400, detail="No hay valores para insert")
#             sql = f"insert into cliente SET {', '.join(campos_insert)}"
#             print(f'----->query del insert -> {sql}')
#             res_cursor.execute(sql)
#             conn.commit()
#             msg = {'status': 0, 'mensaje': "Se inserto el cliente correctamente"}
#         return JSONResponse(content=msg, status_code=200)
#     except HTTPException as ex:
#         msg = {'status': -1,
#                "mensaje:": ex.detail}
#         return JSONResponse(content=msg, status_code=200)
#     except Exception as ex:
#         msg = {'status': -2,
#                "mensaje:": ex.__doc__}
#         return JSONResponse(content=msg, status_code=404)
#     finally:
#         print('---->close del cursor<----')
#         res_cursor.close()


# # @cliente.delete("/cliente/{id}", tags=["Cliente"], name="Eliminar cliente")
# def delete_cliente(id: int):
#     sql = "delete from cliente where id_cliente={0}".format(id)
#     return __delete_update_cliente(sql=sql)


# def __delete_update_cliente(sql: str, band: bool = True):
#     try:
#         res_cursor = conn.cursor()
#         res_cursor.execute(sql)
#         cant = res_cursor.rowcount
#         print(
#             f'----->query del upd/dlt -> {sql} y se modificaron {cant} registros')
#         if band:
#             msg = {'status': 0, 'mensaje': "El registro ya fue eliminado"}
#         else:
#             msg = {'status': 0, 'mensaje': "El registro ya fue actualizado"}
#         if cant == 1:
#             conn.commit()
#             if band:
#                 msg = {'status': 0, 'mensaje': "Se elimno el cliente correctamente"}
#             else:
#                 msg = {'status': 0,
#                        'mensaje': "Se actualizo el cliente correctamente"}
#         else:
#             conn.rollback
#         return JSONResponse(content=msg, status_code=200)
#     except Exception as ex:
#         msg = {'status': -1,
#                "mensaje:": ex.__doc__}
#         return JSONResponse(content=msg, status_code=404)
#     finally:
#         print('---->close del cursor<----')
#         res_cursor.close()


# @cliente.put("/cliente", tags=["Cliente"], name="Actualizar cliente")
# def update_cliente(request: ClienteRequest):
#     try:
#         campos_update = []
#         if request.nombre_cliente is not None:
#             campos_update.append(f"nombre_cliente = '{
#                                  request.nombre_cliente}'")
#         if request.apellido_cliente is not None:
#             campos_update.append(f"apellido_cliente = '{
#                 request.apellido_cliente}'")
#         if request.direccion_cliente is not None:
#             campos_update.append(f"direccion_cliente = '{
#                 request.direccion_cliente}'")
#         if request.telefono_cliente is not None:
#             campos_update.append(f"telefono_cliente = '{
#                 request.telefono_cliente}'")
#         if request.email_cliente is not None:
#             campos_update.append(f"email_cliente = '{request.email_cliente}'")
#         if not campos_update:
#             raise HTTPException(
#                 status_code=400, detail="No hay campos para realizar update")
#         sql = f"UPDATE cliente SET {', '.join(campos_update)} WHERE `id_cliente` = {
#             request.id_cliente}"
#         return __delete_update_cliente(sql=sql, band=False)
#     except HTTPException as ex:
#         msg = {'status': -1,
#                "mensaje:": f'{ex.__doc__} <----> {ex.detail}'}
#         return JSONResponse(content=msg, status_code=ex.status_code)
