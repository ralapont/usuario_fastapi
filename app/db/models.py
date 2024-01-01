
from app.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

class User_model(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)
    nombre = Column(String)
    apellido = Column(String)
    direccion = Column(String)
    telefono = Column(Integer)
    correo = Column(String, unique=True)
    creacion = Column(DateTime, default=datetime.now())
    estado = Column(Boolean, default=False)
    venta = relationship("Venta", backref="usuario", cascade="delete, merge")
    
    def __repr__(self):
        return 'id:{}, username:{}, correo: {}'.format(self.id, self.username, self.correo) 

class Venta(Base):
   __tablename__ = "venta"
   id = Column(Integer, primary_key=True, autoincrement=True)
   usuario_id = Column(Integer,ForeignKey("usuario.id", ondelete="CASCADE"))
   venta = Column(Integer)
   ventas_productos = Column(Integer)
    