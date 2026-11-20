from fastapi import FastAPI,Request,Response,status,HTTPException, Depends,APIRouter
from ..database import get_db
from  .. import models,schemas,utils
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional,List
from sqlalchemy.orm import session
from sqlalchemy.orm import Session
from ..routers import oauth2


router = APIRouter(
    prefix="/login",
    tags=['Authenticaton']
)


@router.post('/')
def login(user_credentials:schemas.Userlogin,db:session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Invalid Credentials")

    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Please enter correct password")

    ## generae token
    ## return token
    access_token = oauth2.create_access_token(data = {"user_id":user.id})

    return {"access_token": access_token, "token_type":"bearer"}