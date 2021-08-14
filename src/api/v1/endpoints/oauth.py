from datetime import timedelta

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.api.v1.dependencies.database import UserRepositoryDependencyMarker
from src.services.database.repositories.user import UserRepository
from src.services.utils.exceptions import UserIsNotAuthenticated
from src.services.utils.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, create_jwt_token, authenticate_user

api_router = APIRouter()


@api_router.post("/oauth", tags=["Oauth & Oauth2"], name="oauth:login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        user_repository: UserRepository = Depends(UserRepositoryDependencyMarker),
):
    try:
        user = await authenticate_user(form_data.username, form_data.password, user_repository)
    except UserIsNotAuthenticated as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from ex
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_jwt_token(jwt_content={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
