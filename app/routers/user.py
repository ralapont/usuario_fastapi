from fastapi import APIRouter, HTTPException, status

from app.schemas import User

router = APIRouter(prefix="/user", tags=["users"])

users = []

@router.get("/")
async def get_users():
    return users

@router.get("/{user_id}")
async def get_user(user_id:int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not exists")

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(user_new:User):
    print("El usuario es: {}".format(user_new))
    for user in users:
        if user.id == user_new.id:
            raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="User just exists")
    users.append(user_new)
    return user_new

@router.delete("/{user_id}", status_code=status.HTTP_205_RESET_CONTENT)
async def remove_user(user_id:int):
    for index, user in enumerate(users):
        if user.id == user_id:
            users.pop(index)
            return {"message": "User {} was remove"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not exists")

@router.put('/{user_id}', status_code=status.HTTP_200_OK)
async def update_user(user_id:int, user_new:User):
    print("El new user is: {} id: {}".format(user_new, user_id))
    for index, user in enumerate(users):
        print("User id in users: {} user_id: {}".format(user.id, user_id))
        if user.id == user_id:
            users[index].nombre = user_new.nombre
            users[index].apellido = user_new.apellido
            users[index].direccion = user_new.direccion
            users[index].telefono = user_new.telefono
            return users[index]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not exists")