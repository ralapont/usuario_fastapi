from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[int] = None
    nombre: str
    apellido: str
    direccion: Optional[str] = None
    telefono: int
    correo: str
    creacion: datetime = datetime.now()
