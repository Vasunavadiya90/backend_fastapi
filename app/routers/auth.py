from fastapi import FastAPI,Request,Response,status,HTTPException, Depends,APIRouter
from ..database import get_db
from  .. import models,schemas,utils
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional,List
from sqlalchemy.orm import session
from sqlalchemy.orm import Session
from ..routers import oauth2
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/login",
    tags=['Authenticaton']
)


@router.post('/',response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db:session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")

    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Please enter correct password")

    ## generae token
    ## return token
    access_token = oauth2.create_access_token(data = {"user_id":user.id})

    return {"access_token": access_token, "token_type":"bearer"}