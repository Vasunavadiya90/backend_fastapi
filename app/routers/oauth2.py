from jose import JWTError,jwt
from datetime import datetime, timedelta, timezone
from .. import schemas,  models , database
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from app.config import settings
# SECRET KEY
# ALGORITHM
# EXPIRATION TIME

# load_dotenv(dotenv_path="../.env") 
# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES","30"))



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY = "K7xQm9vR2pL8nT5wY3aF6jH0cB4eD1sU9zGkM2qW7xN5vP8rL3aJ6fC0hT4yB1eS"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)


    return encoded_jwt
 


def verify_access_token(token:str, credentials_exception):
    try: 

        payload = jwt.decode(token,settings.SECRET_KEY,algorithms= [settings.ALGORITHM])

        id:str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)

    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"could not validate credentials",
                                          headers={"WWW-authenticate":"bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user








