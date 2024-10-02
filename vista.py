import bcrypt
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from conexion import crear,get_db
from modelo import base,RegistroUsuario,RegistroProducto
from shemas import usuarioBase as cli, productoBase as prod
from shemas import Login
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
base.metadata.create_all(bind=crear)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods =["*"],
    allow_headers =["*"],
)
'''login'''

@app.get("/usuario/ID", response_model=list[str])
async def  mostrarid(db:Session=Depends(get_db)):
    id=db.query(RegistroUsuario.id_usuario).all()
    return [doc[0] for doc in id]

@app.post("/insertar/usuario", response_model=cli)
async def registrar_cliente(clientemodel:cli, db:Session=Depends(get_db)):
    
    encriptacion=bcrypt.hashpw(clientemodel.contraseña.encode('utf-8'),bcrypt.gensalt())
    nuevouser=RegistroUsuario(
        id_usuario=clientemodel.id_usuario,
        nombre=clientemodel.nombre,
        email=clientemodel.email,
        contraseña=encriptacion.decode('utf-8'),
        rol=clientemodel.rol
        
    )


    db.add(nuevouser)
    db.commit()
    db.refresh(nuevouser)
    return nuevouser


@app.post("/login")
async def login(user:Login, db:Session=Depends(get_db)):
    db_user=db.query(RegistroUsuario).filter(RegistroUsuario.id_usuario==user.id_usuario).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Usuario no existe")
    if not bcrypt.checkpw(user.contraseña.encode('utf-8'),db_user.contraseña.encode('utf-8')):
        raise HTTPException(status_code=400, detail="contraseña incorrecta")
    
    return{
        "mensaje":"inicio de session ok",
            "nombreUsuario":db_user.nombre,
            "rol":db_user.rol
    }

'''login'''

@app.post("/insertar/producto", response_model=prod)
async def registro_producto(productomodel:prod, db:Session=Depends(get_db)):
    datos=RegistroProducto(**productomodel.dict())
    db.add(datos)
    db.commit()
    db.refresh(datos)
    return datos

@app.get("/concultarclientes", response_model=list[cli])
async def consultar_cliente(db:Session=Depends(get_db)):
    datos_cliente=db.query(RegistroUsuario).all()
    return datos_cliente

@app.get("/consultarProductos", response_model=list[prod])
async def consultar_producto(db:Session=Depends(get_db)):
    datos_productos=db.query(RegistroProducto).all()
    return datos_productos



@app.delete("/eliminar/{id_producto}")
async def eliminar_usuario(id_producto:str, db: Session = Depends(get_db)):
    datos = db.query(RegistroProducto).filter(RegistroProducto.id_producto == id_producto).first()
    if not datos:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(datos)
    db.commit()
    return {"mensaje": "Producto eliminado exitosamente"}

@app.put("/modificarProducto/{id_producto}", response_model=prod)
async def modificar(id_producto:str, productomodel:prod, db:Session=Depends(get_db)):
    validar= db.query(RegistroProducto).filter(RegistroProducto.id_producto == id_producto).first()
    if not validar:
        raise HTTPException(status_code=404, detail="ID no encontrado")
    for key, value in productomodel.dict().items():
        setattr(validar, key, value)

    db.commit()
    db.refresh(validar)
    return validar