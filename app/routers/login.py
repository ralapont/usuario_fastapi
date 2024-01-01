from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from app.db.models import User_model
import app.repository.crud as crud
from app.db.database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext


router = APIRouter(prefix="/token", tags=["token"])
oauth2_scheme = OAuth2PasswordBearer("/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRECT_KEY = "c6f59d10a4b67552fcd156fa86fd911e07dc28f5ce4808dd673e937c6919023c"  # openssl rand -hex 32
ALGORITHM = "HS256"

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
    
def create_token(data: dict, time_expired: Optional[datetime] = None):
    data_copy = data.copy()
    if not time_expired:
        expires = datetime.utcnow() + timedelta(minutes=15)
    else:
        expires = datetime.utcnow() + time_expired
    data_copy.update({"exp": expires})
    token_jwt = jwt.encode(data_copy, key=SECRECT_KEY , algorithm=ALGORITHM)
    print("Token jwt: {}".format(token_jwt))
    return token_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        token_decode = jwt.decode(token=token, key=SECRECT_KEY, algorithms=[ALGORITHM])
        username = token_decode.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credencials",
                                headers={"WWW-Authenticate": "Bearer"})
    except JWTError:  
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credencials",
                                headers={"WWW-Authenticate": "Bearer"})
    current_user = get_user(db, username=username)
    print("Current user: {}".format(current_user.__repr__()))
    return current_user

def get_user_disable_current(user: User_model = Depends(get_current_user)):
    if not user.estado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User")
    return user
    
        
@router.post("/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print("Userdata: {} password: {}".format(form_data.username, form_data.password))
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=30)
    access_token_jwt = create_token({"sub": user.username}, access_token_expires)
    print("Access token expires: {}".format(access_token_expires))
    
    if user:
        print("User authenticated : {}".format(user.__repr__()))
    return {
        "access_token": access_token_jwt,
        "token_type": "bearer"
    }