from pydantic import BaseModel;
from typing import Optional
from fastapi import Form

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