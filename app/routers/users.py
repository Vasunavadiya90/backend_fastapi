from fastapi import FastAPI,Request,Response,status,HTTPException, Depends,APIRouter
from ..database import get_db
from  .. import models,schemas,utils
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional,List
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db:Session=Depends(get_db)):
    # hash the pass


    hashed_pass = utils.hash(password=user.password)
    user.password = hashed_pass
        # Check whether email already exists
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    user_data = user.model_dump()
    user_data["password"] = hashed_pass
    new_user = models.User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}",response_model = schemas.UserOut)
def get_user(id:int,db:Session=Depends(get_db)):
    user  = db.query(models.User).filter(models.User.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with ID : {id} does not exist")
    return user