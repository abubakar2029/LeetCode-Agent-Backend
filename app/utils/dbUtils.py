import os, jwt
from fastapi import Depends, Header, HTTPException
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base
from app import models
import dotenv

dotenv.load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)) -> models.User:
    try:
        print("JWT_SECRET:", JWT_SECRET)
        print("JWT_ALGORITHM:", JWT_ALGORITHM)
        scheme, token = authorization.split()
        print("Authorization header:", authorization, "Scheme:", scheme, "Token:", token)
        if scheme.lower() != "bearer":
            raise ValueError
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_email = payload["email"]
        
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.email == user_email).first()
    print("user* :", user.__dict__)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
