from jose import JWTError, jwt
from datetime import datetime, timedelta

# Configuración del JWT
SECRET_KEY = "j_valenzuela"  # Usa una variable de entorno en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def crear_token(data: dict):
    """
    Genera un JWT con un payload personalizado.
    """
    datos_a_firmar = data.copy()
    fecha_expiracion = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos_a_firmar.update({"exp": fecha_expiracion})
    return jwt.encode(datos_a_firmar, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str):
    """
    Valida el JWT recibido y decodifica el contenido.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None