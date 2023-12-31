from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    nombre: str
    apellido: str
    direccion: Optional[str] = None
    telefono: int
    correo: str
    
class UserResponse(BaseModel):
    id: Optional[int] = None
    username: str
    nombre: str
    apellido: str
    direccion: Optional[str] = None
    telefono: int
    correo: str
    creacion: datetime = datetime.now()
    
class UserResumido(BaseModel):
    username: str
    nombre: str
    correo: str
    class Config():
        from_attributes = True

class UserUpdate(BaseModel):        
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[int] = None
    correo: Optional[str] = None
        
