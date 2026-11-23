from fastapi import FastAPI,Request,Response,status,HTTPException, Depends,APIRouter
from ..database import get_db
from  .. import models,schemas,utils
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional,List
from sqlalchemy.orm import Session
from app.routers.oauth2 import get_current_user
from sqlalchemy import func

router = APIRouter()

@router.get("/hello")
def get_posts(db:Session = Depends(get_db),current_user:int = Depends(get_current_user),limit:int = 10,skip:int = 2, search:Optional[str]=""):

    return "hello world"