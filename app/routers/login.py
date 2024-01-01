from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import app.repository.crud as crud
from app.db.database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext


router = APIRouter(prefix="/token", tags=["token"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db, username):
    usuario = crud.get_user_by_username(db, username)
    if usuario:
        print("Usuario: {}".format(usuario.__repr__()))
    return usuario

def verify_password(plane_password:str, hashed_password:str):
    return pwd_context.verify(plane_password, hashed_password)    

def authenticate_user(db, username, password):
    user = get_user(db, username)
    if user:
        print("User authenticated : {}".format(user.__repr__()))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credencials",
                            headers={"WWW-Authenticate": "Bearer"})
        
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credencials",
                            headers={"WWW-Authenticate": "Bearer"})
    return user        

    
        
    pass
    
@router.post("/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print("Userdata: {} password: {}".format(form_data.username, form_data.password))
    user = authenticate_user(db, form_data.username, form_data.password)
    if user:
        print("User authenticated : {}".format(user.__repr__()))
    return {
        "access_token": "tomatito",
        "token_type": "bearer"
    }