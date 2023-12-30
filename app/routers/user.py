from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas import User
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db.models import User_model
import app.repository.crud as crud

router = APIRouter(prefix="/user", tags=["users"])

@router.get("/", response_model=list[User])
async def get(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = crud.get_users(db, skip=skip, limit=limit)
    print("Data: {}".format(data))
    return data

@router.get("/{user_id}", response_model=User)
async def get_user(user_id:int, db: Session = Depends(get_db)):
    data = crud.get_user(db, user_id)
    if data:
        return data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not exists")

@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_new:User, db: Session = Depends(get_db)):
    print("El usuario es: {}".format(user_new))
    data = crud.create_user(db, user_new)
    return data

@router.delete("/{user_id}", response_model=int, status_code=status.HTTP_205_RESET_CONTENT)
async def remove_user(user_id:int, db: Session = Depends(get_db)):
    user_delete_id = crud.delete_user(db, user_id)
    if user_delete_id:
        print("El usuario delete es: {}".format(user_delete_id))
        return user_delete_id
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not exists")

@router.put('/{user_id}', response_model=User, status_code=status.HTTP_200_OK)
async def update_user(user_id:int, user_new:User, db: Session = Depends(get_db)):
    print("El new user is: {} id: {}".format(user_new, user_id))
    
    user_update = crud.update_user(db, user_id, user_new)
    if user_update:
        print("El usuario actualizado es: {}".format(user_update.id))
        return user_update
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not exists")