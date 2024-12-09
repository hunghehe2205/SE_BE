from fastapi import APIRouter, HTTPException, Depends, status
from database import db_config
from models.users import UserModel
from pydantic import BaseModel


def get_connection():
    return UserModel(db_config=db_config)


router = APIRouter()


@router.get('/users/{user_id}')
async def get_full_user(user_id: str, user_model: UserModel = Depends(get_connection)):
    result = user_model.get_full_user_id_info(user_id)

    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])

    return result


@router.post('/users/', status_code=status.HTTP_201_CREATED)
async def register_user(user_id: str, fullname: str, user_name: str,  password: str, user_model: UserModel = Depends(get_connection)):
    result = user_model.register_user(user_id, fullname, user_name, password)

    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])

    return result


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post('/users/login', status_code=status.HTTP_200_OK)
async def login(data: LoginRequest, user_model: UserModel = Depends(get_connection)):
    result = user_model.log_in(data.username, data.password)

    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])

    return result


@router.get('/users', status_code=status.HTTP_200_OK)
async def get_user_info(user_id: str, user_model: UserModel = Depends(get_connection)):
    result = user_model.get_user_info(user_id)
    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])

    return result
