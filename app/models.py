# On a ici la configuration de la database

from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
