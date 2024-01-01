from fastapi import APIRouter, HTTPException, status, Depends
from app.db.models import User_model
from app.routers.login import get_user_disable_current
from app.schemas import User, UserResponse, UserResumido, UserUpdate
from app.db.database import get_db
from sqlalchemy.orm import Session
import app.repository.crud as crud

router = APIRouter(prefix="/user", tags=["users"])
#oauth2_scheme = OAuth2PasswordBearer("/token")

@router.get("/", response_model=list[UserResponse])
async def get(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User_model = Depends(get_user_disable_current)):
    print("Current user: {}".format(current_user))
    data = crud.get_users(db, skip=skip, limit=limit)
    print("Data: {}".format(data))
    if data:
        return data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not exists")
 
@router.get("/{user_id}", response_model=UserResumido)
async def get_user(user_id:int, db: Session = Depends(get_db), current_user: User_model = Depends(get_user_disable_current)):
    print("Current user: {}".format(current_user))
    data = crud.get_user(db, user_id)
    if data:
        return data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not exists")

@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_new:User, db: Session = Depends(get_db), current_user: User_model = Depends(get_user_disable_current)):
    print("Current user: {}".format(current_user))
    print("El usuario es: {}".format(user_new))
    data = crud.create_user(db, user_new)
    return data

@router.delete("/{user_id}", response_model=int, status_code=status.HTTP_205_RESET_CONTENT)
async def remove_user(user_id:int, db: Session = Depends(get_db), current_user: User_model = Depends(get_user_disable_current)):
    print("Current user: {}".format(current_user))
    user_delete_id = crud.delete_user(db, user_id)
    if user_delete_id:
        print("El usuario delete es: {}".format(user_delete_id))
        return user_delete_id
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not exists")

@router.patch('/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id:int, user_new: UserUpdate, db: Session = Depends(get_db), current_user: User_model = Depends(get_user_disable_current)):
    print("Current user: {}".format(current_user))
    print("El new user is: {} id: {}".format(user_new, user_id))
    
    user_update = crud.update_user(db, user_id, user_new)
    if user_update:
        print("El usuario actualizado es: {}".format(user_update.id))
        return user_update
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not exists")
