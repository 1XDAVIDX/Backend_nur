from fastapi import Security,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from tokens import verificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  # Ruta para obtener token

def obtener_usuario_autenticado(token: str = Depends(oauth2_scheme)):
    """
    Valida el token y retorna el usuario autenticado.
    """
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    return payload