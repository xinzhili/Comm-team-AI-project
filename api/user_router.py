from fastapi import APIRouter, HTTPException, Body
from starlette import status
from starlette.responses import JSONResponse

from models.user import User
from schemas.user import UserResponse, UserCreate, PasswordChange, UserLoginRequest

user_router = APIRouter(
    tags=['Users'],
    prefix='/api/v1/users'
)


@user_router.post(path='/register',
                  status_code=status.HTTP_201_CREATED,
                  summary='Register User',
                  description='Register new User',
                  response_model=UserResponse)
async def register(user: UserCreate = Body(...)):
    return await User.register(user)

@user_router.post(path='/login',
                  status_code=status.HTTP_201_CREATED,
                  summary='Login',
                  description='Login Application')
async def login(user_login: UserLoginRequest = Body()):
    user = await User.get_user_by_user_name(user_login.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {user_login.username} not existing'
        )

    is_password_matched = User.verify_password(
        plain_password=user_login.password,
        hashed_password=user.hashed_password
    )

    if not is_password_matched:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Password incorrect'
        )
    else:
        return JSONResponse(content='Login successfully')


@user_router.post(path='/reset-password',
                  status_code=status.HTTP_201_CREATED,
                  summary='Reset Password',
                  description='Reset Login password')
async def reset_password(password_change: PasswordChange):
    await User.change_password(
        user_name=password_change.user_name,
        current_password=password_change.current_password,
        new_password=password_change.new_password
    )






