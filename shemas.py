from pydantic import BaseModel;
from typing import Optional
from fastapi import Form
from datetime import date

class usuarioBase(BaseModel):
    id_usuario:str
    nombre:str
    #email:str
    contraseña:str
    rol:str

class productoBase(BaseModel):
    id_producto:str=Form(...)
    nombre:str=Form(...)
    descripcion:str=Form(...)
    precio:float=Form(...)
    stock:int=Form(...)
    categotia:str=Form(...)
    imagen: Optional[str]=None
    cantidadProducto: Optional[int]=None

class Login(BaseModel):
    id_usuario:str
    contraseña:str

class CompraCreate(BaseModel):
    
    id_producto:str
    id_usuario:str
    cantidad:Optional[int]
    

class carritoCompra(BaseModel):
    
    id_producto:str
    id_usuario:str
    cantidad:Optional[int]
    
class Email(BaseModel):
    destinatario: str
    asunto: str
    mensaje: str

class EditarUsuario(BaseModel):
    id_usuario: Optional[str] = None
    nombre: Optional[str] = None
    contraseña: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    tarjetaCredito: Optional[str] = None


class EditarCompraTerminada(BaseModel):
    
    fecha: Optional[date] = None
    estado: Optional[str] = None
    guiaTranporte: Optional[str] = None