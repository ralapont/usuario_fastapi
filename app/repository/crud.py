from sqlalchemy.orm import Session
from app.db import models
from app.schemas import User


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User_model).offset(skip).limit(limit).all()

def create_user(db: Session, user: User):
    db_user = models.User_model(username = user.username,
                                password = user.password,
                                nombre = user.nombre, 
                                apellido = user.apellido, 
                                direccion = user.direccion, 
                                correo = user.correo, 
                                telefono = user.telefono,
                                creacion = user.creacion,
                                estado = True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    user_db = db.query(models.User_model).filter(models.User_model.id == user_id).first()
    if not user_db:
        return None
    return user_db

def delete_user(db: Session, user_id: int):
    user_old = db_hero = db.get(models.User_model, user_id)
    if not user_old:
        return None
    db.delete(user_old)
    db.commit()
    return user_id

def update_user(db: Session, user_id:int, user_new: User):
    db_user = db.get(models.User_model, user_id)
    if not db_user:
        return None
    for key, value in vars(user_new).items():
        setattr(db_user, key, value) if value else None
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user        
