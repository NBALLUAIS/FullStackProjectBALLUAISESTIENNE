from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.database import get_db
from app.models import User
from app.auth import create_access_token, verify_token
from app.schemas import UserCreate, Token

router = APIRouter(prefix="/users", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = user.password 
    new_user = User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = create_access_token({"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or user.hashed_password != form_data.password:  
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}
