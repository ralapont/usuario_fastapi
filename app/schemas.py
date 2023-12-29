from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    nombre: str
    apellido: str
    direccion: Optional[str] = None
    telefono: int
    creacion_user: datetime = datetime.now()
