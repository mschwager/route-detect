from typing import Annotated, Union

from fastapi import APIRouter, Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# ruleid: fastapi-route-unauthenticated
@app.get("/")
def read_root():
    return {"Hello": "World"}


# ruleid: fastapi-route-unauthenticated
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# ruleid: fastapi-route-unauthenticated
@router.get("/users/")
def read_users():
    return [{"name": "Rick"}, {"name": "Morty"}]


app.include_router(router)


# ruleid: fastapi-route-authenticated
@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


# ruleid: fastapi-route-authenticated
@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
