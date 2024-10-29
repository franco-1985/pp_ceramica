# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Table
from sqlalchemy.dialects.mysql import INTEGER, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Cliente(Base):
    __tablename__ = 'cliente'

    id_cliente = Column(INTEGER(11), primary_key=True, index=True)
    nombre_cliente = Column(String(100))
    apellido_cliente = Column(String(100))
    direccion_cliente = Column(String(100))
    telefono_cliente = Column(String(13))
    email_cliente = Column(String(100))

    pedidos = relationship("Pedido", back_populates="cliente")


class Estado(Base):
    __tablename__ = 'estado'

    id_estado = Column(INTEGER(11), primary_key=True)
    nombre_estado = Column(String(50))


class Fase(Base):
    __tablename__ = 'fase'

    id_fase = Column(INTEGER(11), primary_key=True)
    nombre_fase = Column(String(50), nullable=False)


class Insumo(Base):
    __tablename__ = 'insumo'

    id_insumo = Column(INTEGER(11), primary_key=True)
    nombre_insumo = Column(String(50), nullable=False)


t_insumosporproducto = Table(
    'insumosporproducto', metadata,
    Column('nombre_producto', String(100)),
    Column('cantidad', Float(asdecimal=True)),
    Column('nombre_insumo', String(50)),
    Column('nombre_unidad_medida', String(50))
)


t_productoporfase = Table(
    'productoporfase', metadata,
    Column('nombre_producto', String(100)),
    Column('nombre_fase', String(50)),
    Column('cantidad_tiempo', INTEGER(11)),
    Column('nombre_unidad_medida', String(50))
)


class UnidadMedida(Base):
    __tablename__ = 'unidad_medida'

    id_unidad_medida = Column(INTEGER(11), primary_key=True)
    nombre_unidad_medida = Column(String(50), nullable=False)
    abreviatura_unidad_medida = Column(String(10), nullable=False)


class Producto(Base):
    __tablename__ = 'producto'

    id_producto = Column(INTEGER(11), primary_key=True)
    nombre_producto = Column(String(100), nullable=False)
    precio_producto = Column(Float(asdecimal=True))
    medida_producto = Column(Float(asdecimal=True))
    id_unidad_medida = Column(ForeignKey(
        'unidad_medida.id_unidad_medida'), index=True)
    imagen = Column(String(100))

    unidad_medida = relationship('UnidadMedida')


class Tiempo(Base):
    __tablename__ = 'tiempo'

    id_tiempo = Column(INTEGER(11), primary_key=True)
    cantidad_tiempo = Column(INTEGER(11), nullable=False)
    id_unidad_medida = Column(ForeignKey(
        'unidad_medida.id_unidad_medida'), nullable=False, index=True)

    unidad_medida = relationship('UnidadMedida')


class DetallePedido(Base):
    __tablename__ = 'detalle_pedido'

    id_detalle_pedido = Column(INTEGER(11), primary_key=True)
    id_pedido = Column(INTEGER(11))
    cantidad_producto = Column(INTEGER(11), nullable=False)
    total = Column(DECIMAL(11, 3))
    id_producto = Column(ForeignKey('producto.id_producto'), index=True)
    id_estado_pedido = Column(INTEGER(11), nullable=False)

    producto = relationship('Producto')


    def __str__(self) -> str:
        return 'estoy mostrando el str del objeto unico'


class Productoxfase(Base):
    __tablename__ = 'productoxfase'

    id_producto = Column(ForeignKey('producto.id_producto'),
                         primary_key=True, nullable=False)
    id_fase = Column(ForeignKey('fase.id_fase'),
                     primary_key=True, nullable=False, index=True)
    observaciones = Column(String(300))
    id_tiempo = Column(ForeignKey('tiempo.id_tiempo'), index=True)

    fase = relationship('Fase')
    producto = relationship('Producto')
    tiempo = relationship('Tiempo')


class Productoxinsumo(Base):
    __tablename__ = 'productoxinsumo'

    id_producto = Column(ForeignKey('producto.id_producto'),
                         primary_key=True, nullable=False)
    id_insumo = Column(ForeignKey('insumo.id_insumo'),
                       primary_key=True, nullable=False, index=True)
    id_unidad_medida = Column(ForeignKey(
        'unidad_medida.id_unidad_medida'), index=True)
    cantidad = Column(Float(asdecimal=True), primary_key=True, nullable=False)

    insumo = relationship('Insumo')
    producto = relationship('Producto')
    unidad_medida = relationship('UnidadMedida')


class Pedido(Base):
    __tablename__ = 'pedido'

    id_pedido = Column(INTEGER(11), primary_key=True)
    fecha_pedido = Column(DateTime)
    fecha_entrega_aproximado = Column(DateTime)
    fecha_entrega_real = Column(DateTime)
    id_estado_pedido = Column(INTEGER(11))
    # id_cliente = Column(INTEGER(11))
    id_cliente = Column(INTEGER, ForeignKey('cliente.id_cliente'))
    # id_detalle_pedido = Column(ForeignKey('detalle_pedido.id_detalle_pedido'))

    # detalle_pedido = relationship('DetallePedido')
    cliente = relationship("Cliente", back_populates="pedidos")