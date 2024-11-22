from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #initilisation de la fonction de hashing

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def initialize_database():
    Base.metadata.create_all(bind=engine)

def generate_user(name: str, email: str, password: str):
    db: Session = SessionLocal()

    try:
        existing_user = db.query(User).filter(User.email == email).first() # On cherche ici a verifier si le user existe deja pour eviter les doublons
        if existing_user:
            print(f"User with email '{email}' already exists.")
            return

        hashed_password = hash_password(password)

        new_user = User(
            name=name,
            email=email,
            hashed_password=hashed_password
        )
        db.add(new_user) #On injecte le nouveau user dans la database
        db.commit()
        db.refresh(new_user)

        print(f"User '{name}' with email '{email}' has been created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    initialize_database()

    name = input("Enter user name: ")
    email = input("Enter user email: ")
    password = input("Enter user password: ")

    generate_user(name=name, email=email, password=password)
