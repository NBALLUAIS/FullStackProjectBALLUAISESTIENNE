# On cree ici les data structures pour user et token verification

from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
