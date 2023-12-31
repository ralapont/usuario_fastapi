from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/token", tags=["token"])

@router.post("/")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print("Userdata: {} password: {}".format(form_data.username, form_data.password))
    return {
        "access_token": "tomatito",
        "token_type": "bearer"
    }