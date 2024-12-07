from fastapi import APIRouter, HTTPException, Depends, status
from database import db_config
from models.users import UserModel


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


@router.post('/users/{user_name}/{pass_word}', status_code=status.HTTP_200_OK)
async def login(user_name: str, password: str, user_model: UserModel = Depends(get_connection)):
    result = user_model.log_in(user_name, password)

    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])

    return result
