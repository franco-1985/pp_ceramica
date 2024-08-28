from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.models import Cliente
from sqlalchemy import func


DETAILS_EXCEPTION = 'Cliente no encontrado'


def select_clientes(db):
    res = db.query(Cliente).all()
    if not res:
        raise HTTPException(
            status_code=201, detail="No hay listado")
    return res


def select_cliente_by_id(db, id: int):
    res = db.query(Cliente).get(id)
    if res == None:
        raise HTTPException(
            status_code=201, detail=DETAILS_EXCEPTION)
    return res


def insert_cliente(db, cliente: Cliente):
    res = db.query(func.max(Cliente.id_cliente)).scalar()
    cliente.id_cliente = res + 1
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    msg = {'status': 0,
           'mensaje': f"Se inserto el cliente correctamente con el id {res}"}
    return JSONResponse(content=msg, status_code=200)


def update_cliente(db, nuevos_datos: dict):
    cliente = db.query(Cliente).get(nuevos_datos['id_cliente'])
    if cliente:
        for key, value in nuevos_datos.items():
            setattr(cliente, key, value)
        db.commit()
        db.refresh(cliente)
        msg = {'status': 0,
               'mensaje': f"Se modifico el cliente correctamente con los nuevos datos."}
        return JSONResponse(content=msg, status_code=200)
    else:
        raise HTTPException(
            status_code=201, detail=DETAILS_EXCEPTION)
