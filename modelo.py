from sqlalchemy import String,Integer,Column,ForeignKey, Numeric,Date
from conexion import base
from sqlalchemy.orm import relationship

class RegistroProducto(base):
    __tablename__ = "producto"
    id_producto = Column(String(20), primary_key=True, index=True, unique=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(400), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    categotia = Column(String(50),nullable=True)
    imagen=Column(String(255),nullable=True)
    cantidadProducto = Column(Integer, nullable=True)

class RegistroUsuario(base):
    __tablename__ = "usuario"
    id_usuario = Column(String(320), primary_key=True, unique=True, index=True)
    nombre = Column(String(50), nullable=True)
    #email = Column(String(50), nullable=True)
    contraseña = Column(String(100), nullable=False)  
    rol=Column(String(20), nullable=False )



class Compra(base):
    __tablename__ = "compra"
    id_compra = Column(Integer, autoincrement=True, primary_key=True, index=True)
    id_producto = Column(String(20), ForeignKey('producto.id_producto'), index=True)
    id_usuario = Column(String(320), ForeignKey('usuario.id_usuario'), index=True)
    cantidad = Column(Integer, nullable=True)
    total = Column(Numeric(10, 2), nullable=True)
    nombre_producto = Column(String(50), nullable=False)

    fecha = Column(Date, nullable=True)
    estado = Column(String(20), nullable=False, default='pendiente')
    guiaTranporte = Column(String(100), nullable=True)


class CompraGrafico(base):
    __tablename__ = "CompraGrafico"
    id_compraGrafico = Column(Integer, autoincrement=True, primary_key=True, index=True)
    id_producto = Column(String(20), ForeignKey('producto.id_producto'), index=True)
    id_usuario = Column(String(320), ForeignKey('usuario.id_usuario'), index=True)
    id_compra = Column(Integer, nullable=True)
    cantidad = Column(Integer, nullable=True)
    total = Column(Numeric(10, 2), nullable=True)
    nombre_producto = Column(String(50), nullable=False)

class compraTerminada(base):
    __tablename__ = "compraTerminada"
    id_CompraTerminada = Column(Integer, autoincrement=True, primary_key=True, index=True)
    id_producto = Column(String(20), ForeignKey('producto.id_producto'), index=True)
    id_usuario = Column(String(320), ForeignKey('usuario.id_usuario'), index=True)
    id_compra = Column(Integer, nullable=True)
    cantidad = Column(Integer, nullable=True)
    total = Column(Numeric(10, 2), nullable=True)
    nombre_producto = Column(String(50), nullable=False)

    fecha = Column(Date, nullable=True)
    estado = Column(String(20), nullable=False, default='pendiente')
    guiaTranporte = Column(String(100), nullable=True)

class carritoCompra(base):
    __tablename__ = "carritoCompra"
    id_carrito = Column(Integer, autoincrement=True, primary_key=True, index=True)
    id_producto = Column(String(20), ForeignKey('producto.id_producto'), index=True)
    id_usuario = Column(String(320), ForeignKey('usuario.id_usuario'), index=True)
    compra_id = Column(Integer, ForeignKey('compra.id_compra'), nullable=True)
    cantidad = Column(Integer, nullable=False, default=1)
    total = Column(Numeric(10, 2), nullable=True)