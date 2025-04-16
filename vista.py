import bcrypt
from fastapi import FastAPI, UploadFile, File,Form, Depends, HTTPException
from sqlalchemy.orm import Session
from conexion import crear,get_db
from modelo import base,RegistroUsuario,RegistroProducto,Compra,carritoCompra,compraTerminada,CompraGrafico
from shemas import usuarioBase as cli, productoBase as prod, CompraCreate as com, carritoCompra as carri, Email, EditarUsuario
from shemas import Login
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.staticfiles import StaticFiles
from enviar_email import enviar_email

from verificarjwt import obtener_usuario_autenticado
from fastapi.security import OAuth2PasswordRequestForm
from tokens import crear_token

app=FastAPI()
app.mount("/file_img", StaticFiles(directory="file_img"), name="file_img")
base.metadata.create_all(bind=crear)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods =["*"],
    allow_headers =["*"],
)
'''login'''


@app.post("/enviar-email/")
async def enviar_correo(email: Email):
    resultado = enviar_email(email.destinatario, email.asunto, email.mensaje)
    return resultado




@app.put("/editar/usuario/{id_usuario}", response_model=cli)
async def editar_usuario(id_usuario: str, usuario_model: EditarUsuario, db: Session = Depends(get_db)):
    usuario = db.query(RegistroUsuario).filter(RegistroUsuario.id_usuario == id_usuario).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualiza los campos del usuario
    for key, value in usuario_model.dict(exclude_unset=True).items():
        if key == "contraseña":  # Si el campo es contraseña, codificarla
            value = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        setattr(usuario, key, value)
    
    db.commit()
    db.refresh(usuario)
    
    return usuario


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
        #email=clientemodel.email,
        contraseña=encriptacion.decode('utf-8'),
        rol=clientemodel.rol
        
    )

    enviar_email(clientemodel.id_usuario,"Bienvenido a la tienda de mascotas","Gracias por registrarte en nuestra tienda de mascotas")


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
    #enviar_email(user.id_usuario,"Bienvenido a la tienda de mascotas","Gracias por iniciar sesion en nuestra tienda de mascotas")
    
    # Genera el token con el payload del usuario
    payload = {
        "id_usuario": db_user.id_usuario,
        "nombre": db_user.nombre,
        "direccion": db_user.direccion,
        "telefono": db_user.telefono,
        "tarjetaCredito": db_user.tarjetaCredito,
        #"email": db_user.email,
        "rol": db_user.rol
    }
    token = crear_token(payload)

    return {"access_token": token, "token_type": "bearer"}

@app.get("/mi-perfil")
async def perfil(usuario: dict = Depends(obtener_usuario_autenticado)):
    return {"mensaje": "Acceso autorizado", "datos": usuario}

'''login'''

'''Modificacion del insertar producto'''
'''antes'''
'''@app.post("/insertar/producto", response_model=prod)
async def registro_producto(productomodel:prod, db:Session=Depends(get_db)):
    datos=RegistroProducto(**productomodel.dict())
    db.add(datos)
    db.commit()
    db.refresh(datos)
    return datos'''
'''antes'''

'''nuevo'''
@app.post("/insertar/producto")
async def registro_producto(
    id_producto:str=Form(...),
    nombre:str=Form(...),
    descripcion:str=Form(...),
    precio:float=Form(...),
    stock:int=Form(...),
    categotia:str=Form(...),
    file: UploadFile = File(...),   
    db:Session=Depends(get_db)
):
    file_location=f"file_img/{file.filename}"
    os.makedirs("file_img",exist_ok=True)

    with open(file_location,"wb") as buffer:
        buffer.write(await file.read())

    producto_data={
        "id_producto": id_producto,
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "stock": stock,
        "categotia": categotia,
        "imagen": file_location,
    }
    db_data= RegistroProducto(** producto_data)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)

    return db_data


'''nuevo'''
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


@app.put("/modificarProducto/{id_producto_validar}", response_model=prod)
async def modificar(
    id_producto_validar : str ,
    id_producto: str = Form(...),
    nombre: str = Form(...),
    descripcion: str = Form(...),
    precio: float = Form(...),
    stock: int = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    
    validar = db.query(RegistroProducto).filter(RegistroProducto.id_producto == id_producto_validar).first()
    
    if not validar:
        raise HTTPException(status_code=404, detail="ID no encontrado")
    
    validar2 = db.query(RegistroProducto).filter(RegistroProducto.id_producto == id_producto).first()
    if validar2 and validar2.id_producto != id_producto_validar:
        raise HTTPException(status_code=500, detail="ID ya utilizado")

    validar.id_producto = id_producto
    validar.nombre = nombre
    validar.descripcion = descripcion
    validar.precio = precio
    validar.stock = stock

    
    if file:
        file_location = f"file_img/{file.filename}"
        os.makedirs("file_img", exist_ok=True)

        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
        
        validar.imagen = file_location  

    
    db.commit()
    db.refresh(validar)

    return validar



@app.post("/compra")
async def compra_procto(compramodel: com, db: Session = Depends(get_db)):
    # Buscar el producto
    validar = db.query(RegistroProducto).filter(RegistroProducto.id_producto == compramodel.id_producto).first()
    if not validar:
        raise HTTPException(status_code=404, detail="ID no encontrado")
    
    if validar.stock < compramodel.cantidad:
        raise HTTPException(status_code=404, detail="Producto agotado")
    
    total1 = compramodel.cantidad * validar.precio

    # Crea la instancia del modelo SQLAlchemy "Compra"
    compra_db = Compra(
        id_producto=validar.id_producto,
        id_usuario=compramodel.id_usuario,
        cantidad=compramodel.cantidad,
        total=total1,
        nombre_producto=validar.nombre  # Guarda el nombre del producto
    )

    # Actualiza el stock del producto
    validar.stock -= compramodel.cantidad

    mensaje = f"""
        Compra realizada,

        Gracias por tu compra.
        Producto: {compra_db.nombre_producto}
        Cantidad: {compra_db.cantidad}
        Total: ${compra_db.total}

        ¡Esperamos que disfrutes tu producto!
        """

    enviar_email(compramodel.id_usuario, "Compra realizada", mensaje)

    db.add(compra_db)
    db.commit()
    db.refresh(compra_db)


    compra_grafico_db = CompraGrafico(
        id_producto=compra_db.id_producto,
        id_usuario=compra_db.id_usuario,
        cantidad=compra_db.cantidad,
        total=compra_db.total,
        id_compra=compra_db.id_compra,
        nombre_producto=compra_db.nombre_producto
    )

    db.add(compra_grafico_db)
    db.commit()

    

    return {
        "id_compra": compra_db.id_compra,
        "id_producto": validar.id_producto,
        "nombre_producto": validar.nombre,
        "descripcion": validar.descripcion,
        "precio": validar.precio,
        "stock": validar.stock,
        "total": compra_db.total
    }

@app.get("/compra")
async def referenciaCompra(db:Session=Depends(get_db)):
    datos_compra= db.query(Compra).all()
    return datos_compra





@app.get("/compra_grafico_ver")
async def compraGraficoVer(db:Session=Depends(get_db)):
    datos_grafico = db.query(CompraGrafico).all()
    return datos_grafico


@app.delete("/completada/{id_compra}/{usuario}")
async def completado(id_compra: int, usuario: str, db: Session = Depends(get_db)):
    validacion_compra = db.query(Compra).filter(Compra.id_compra == id_compra).first()
    validacion_usuario = db.query(RegistroUsuario).filter(RegistroUsuario.id_usuario == usuario).first()

    if not validacion_compra or not validacion_usuario:
        raise HTTPException(status_code=404, detail="Compra o usuario no encontrado")

    # Crea la instancia en la tabla de compras terminadas usando el modelo 'compraTerminada'
    compra_terminada_instance = compraTerminada(
        id_producto=validacion_compra.id_producto,
        id_usuario=validacion_usuario.id_usuario,
        cantidad=validacion_compra.cantidad,
        total=validacion_compra.total,
        id_compra=validacion_compra.id_compra,  # Opcional: almacenar el id original
        nombre_producto=validacion_compra.nombre_producto
    )

    db.add(compra_terminada_instance)
    db.commit()

    # Elimina la compra original de la tabla 'compra'
    db.delete(validacion_compra)
    db.commit()

    mensaje = f"""
        Producto Enviado,

        Gracias por tu compra.
        Producto: {compra_terminada_instance.nombre_producto}
        Cantidad: {compra_terminada_instance.cantidad}
        Total: ${compra_terminada_instance.total}

        ¡Esperamos que disfrutes tu producto!
        """

    enviar_email(compra_terminada_instance.id_usuario, "Compra realizada", mensaje)

    return {
        "id_producto": validacion_compra.id_producto,
        "cantidad": validacion_compra.cantidad,
        "total": validacion_compra.total,
        "id_compra": validacion_compra.id_compra,
        "id_usuario": validacion_usuario.id_usuario,
        "nombre": validacion_usuario.nombre,
        #"email": validacion_usuario.email,
    }

@app.delete("/completadas/{id_usuario}")
async def completadas(id_usuario: str, db: Session = Depends(get_db)):
    # Validar que el usuario exista
    validacion_usuario = db.query(RegistroUsuario).filter(RegistroUsuario.id_usuario == id_usuario).first()
    if not validacion_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Obtener todas las compras del usuario
    compras_usuario = db.query(Compra).filter(Compra.id_usuario == id_usuario).all()
    if not compras_usuario:
        raise HTTPException(status_code=404, detail="No hay compras para este usuario")

    # Lista para almacenar las compras completadas
    compras_terminadas = []

    for compra in compras_usuario:
        # Crear la instancia en la tabla de compras terminadas
        compra_terminada_instance = compraTerminada(
            id_producto=compra.id_producto,
            id_usuario=compra.id_usuario,
            cantidad=compra.cantidad,
            total=compra.total,
            id_compra=compra.id_compra,  # Opcional: almacenar el id original
            nombre_producto=compra.nombre_producto
        )
        db.add(compra_terminada_instance)

        # Agregar la compra a la lista de completadas
        compras_terminadas.append({
            "id_producto": compra.id_producto,
            "cantidad": compra.cantidad,
            "total": compra.total,
            "id_compra": compra.id_compra,
            "id_usuario": compra.id_usuario,
            "nombre_producto": compra.nombre_producto
        })

        # Eliminar la compra original de la tabla 'compra'
        db.delete(compra)

    # Confirmar los cambios en la base de datos
    db.commit()
    

    # Crear resumen para el correo
    resumen = "Producto Enviado,\n\nGracias por tu compra.\n\n"
    total_general = 0

    for compra in compras_terminadas:
        resumen += (
            f"Producto: {compra['nombre_producto']}\n"
            f"Cantidad: {compra['cantidad']}\n"
            f"Subtotal: ${compra['total']}\n\n"
        )
        total_general += compra["total"]

    resumen += f"Total general: ${total_general}\n\n¡Esperamos que disfrutes tus productos!"

    # Enviar el correo
    enviar_email(id_usuario, "Compra realizada", resumen)

    # Retornar resumen de las compras completadas
    return {
        "message": "Todas las compras del usuario han sido completadas",
        "compras_completadas": compras_terminadas
    }


@app.post("/carrito")
async def compra_procto(compramodel:carri, db:Session=Depends(get_db)):
    validar = db.query(RegistroProducto).filter(RegistroProducto.id_producto == compramodel.id_producto).first()
    
    if not validar:
        raise HTTPException(status_code=404, detail="ID no encomtrado")
    
    datos = carritoCompra(**compramodel.dict())
    if validar.stock <  compramodel.cantidad:
        raise HTTPException(status_code=404, detail="Producto agotado")
   
    total1 = datos.cantidad * validar.precio
    datos.total = total1
    

    db.add(datos)
    db.commit()
    db.refresh(datos)
    return{
        "id_carrito":datos.id_carrito,
        "id_producto":validar.id_producto,
        "nombre":validar.nombre,
        "descripcion":validar.descripcion,
        "precio":validar.precio,
        "stock":validar.stock,
        "total":datos.total
    }

@app.get("/carritoProductos")
async def referenciaCompra(db:Session=Depends(get_db)):
    datos_compra= db.query(carritoCompra).all()
    return datos_compra

@app.get("/compraTerminado")
async def compraTermin(db:Session=Depends(get_db)):
    datos_compraTerminado= db.query(compraTerminada).all()
    return datos_compraTerminado


@app.delete("/quitar/{id_carrito}")
async def completado(id_carrito:int, db:Session=Depends(get_db)):
    validacion_compra= db.query(carritoCompra).filter(carritoCompra.id_carrito == id_carrito).first()
    

    db.delete(validacion_compra)
    db.commit()
    return "quitado"
    

@app.post("/carritoMultiple/{id_usuario}")
async def compra_producto_multiple(id_usuario: str, db: Session = Depends(get_db)):
    # Obtener todos los productos del carrito para el usuario
    listar_compras = db.query(carritoCompra).filter(carritoCompra.id_usuario == id_usuario).all()
    
    if not listar_compras:
        raise HTTPException(status_code=404, detail="El usuario no tiene productos en el carrito")
    
    # Lista para almacenar las compras realizadas
    compras_realizadas = []
    
    for item in listar_compras:
        # Validar que el producto existe en la tabla RegistroProducto
        validar = db.query(RegistroProducto).filter(RegistroProducto.id_producto == item.id_producto).first()
        
        if not validar:
            raise HTTPException(status_code=404, detail=f"Producto con ID {item.id_producto} no encontrado")
        
        # Verificar stock disponible del producto
        if validar.stock < item.cantidad:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para el producto {validar.nombre} (ID: {item.id_producto})")
        
        # Calcular el total (cantidad * precio)
        total = item.cantidad * validar.precio
        
        # Reducir el stock del producto
        validar.stock -= item.cantidad
        
        # Crear el registro de la compra
        datos = Compra(
            id_usuario=id_usuario,
            id_producto=item.id_producto,
            cantidad=item.cantidad,
            total=total,

            nombre_producto=validar.nombre
        )
        db.add(datos)
        compras_realizadas.append({
            "id_producto": validar.id_producto,
            "nombre": validar.nombre,
            "descripcion": validar.descripcion,
            "precio_unitario": validar.precio,
            "cantidad_comprada": item.cantidad,
            "total": total,
            "stock_restante": validar.stock
        })
    
    # Limpiar el carrito del usuario después de la compra
    db.query(carritoCompra).filter(carritoCompra.id_usuario == id_usuario).delete()
    
    # Confirmar los cambios en la base de datos
    db.commit()
    
    # Retornar resumen de la compra
    return {
        "message": "Compra realizada con éxito",
        "compras": compras_realizadas
    }
