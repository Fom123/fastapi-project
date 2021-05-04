from datetime import timedelta

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from api import api_router
from services.db.crud import UserRepository
from services.dependencies.containers import Application
from services.utils.security import authenticate_user, \
    ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token


@api_router.post("/oauth", tags=["Test"], dependencies=None)
@inject
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        user_crud: UserRepository = Depends(
            Provide[Application.services.user_repository]
        )
):
    user = await authenticate_user(form_data.username, form_data.password,
                                   user_crud)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
