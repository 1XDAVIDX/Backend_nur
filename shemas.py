from pydantic import BaseModel;

class usuarioBase(BaseModel):
    id_usuario:str
    nombre:str
    email:str
    contraseña:str
    rol:str

class productoBase(BaseModel):
    id_producto:str
    nombre:str
    descripcion:str
    precio:float
    stock:int

class Login(BaseModel):
    id_usuario:str
    contraseña:str