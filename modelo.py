from sqlalchemy import String,Integer,Column,ForeignKey, Numeric,Date
from conexion import base
from sqlalchemy.orm import relationship

class RegistroProducto(base):
    __tablename__ = "producto"
    id_producto = Column(String(20), primary_key=True, index=True, unique=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(100), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)

class RegistroUsuario(base):
    __tablename__ = "usuario"
    id_usuario = Column(String(20), primary_key=True, unique=True, index=True)
    nombre = Column(String(50), nullable=True)
    email = Column(String(50), nullable=True)
    contraseña = Column(String(100), nullable=False)  
    rol=Column(String(20), nullable=False )



class compra(base):
    __tablename__ = "compra"
    id_compra = Column(Integer, autoincrement=True, primary_key=True, index=True)
    id_producto = Column(String(20), ForeignKey('producto.id_producto'), index=True)
    id_usuario = Column(String(20), ForeignKey('usuario.id_usuario'), index=True)
    cantidad = Column(Integer, nullable=True)
    total = Column(Numeric(10, 2), nullable=True)