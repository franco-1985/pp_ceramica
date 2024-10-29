from fastapi import FastAPI
from src.routes.cliente import cliente
from src.routes.estado import estado
from src.routes.fase import fase
from src.routes.insumo import insumo
from src.routes.unidadmedida import medida
from src.routes.producto import producto
from src.routes.tiempo import tiempo
from src.routes.detallepedido import detpedido
from src.routes.pedido import pedido
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="API catalogo ceramica",
              description="Definicion de metodos para obtener datos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las URLs
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los headers
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(cliente)
app.include_router(estado)
app.include_router(fase)
app.include_router(insumo)
app.include_router(medida)
app.include_router(producto)
app.include_router(tiempo)
app.include_router(pedido)
app.include_router(detpedido)
