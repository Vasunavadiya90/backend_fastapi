from fastapi import FastAPI,Request,Response,status,HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List
from dotenv import load_dotenv
import os
from . import models
from app.database import Base, SessionLocal,engine,get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import schemas,utils
from app.routers import post,users,auth,vote
from .config import settings


load_dotenv()

app = FastAPI()

password_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
# @app.get("/posts",response_model=List[schemas.Post])
# def get_conncetion(db:Session = Depends(get_db)):

#     post = db.query(models.Post).all()
#     return post 

 

# @app.post("/createposts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post) 
# def create_posts(new_post:schemas.Post,db:Session = Depends(get_db) ): #'''However, there is one important thing: In Pydantic V2, .dict() is deprecated. You should use .model_dump() instead'''
#     # new_post = models.Post(title = new_post.title, content=new_post.content) ## it is is inefficient. Use Packing and unpackig the dict.
#     new_post = models.Post(**new_post.model_dump())  ## we packed the dictionary
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     return new_post


# @app.get("/posts/{id}",response_model=schemas.Post)
# def get_posts(id:str,db:Session = Depends(get_db)):

#     post = db.query(models.Post).filter(models.Post.id==id).first()
#     print(type(post))

#     return post


# @app.delete("/posts/{id}",status_code= status.HTTP_204_NO_CONTENT)
# def delete_post(id:int,db:Session = Depends(get_db)):

#     post = db.query(models.Post).filter(models.Post.id==id).first()
    
#     if post ==None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} does not exist")
   
#     db.delete(post)
#     db.commit()


#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}", response_model=schemas.Post)
# def update_post(
#     id: int,
#     updated_post: schemas.PostCreate,
#     db: Session = Depends(get_db)
# ):

#     post_query = db.query(models.Post).filter(
#         models.Post.id == id
#     )

#     post = post_query.first()

#     if post is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id {id} not found"
#         )

#     post_query.update(
#         updated_post.model_dump(),
#         synchronize_session="auto"
#     )

#     db.commit()

#     updated_post_db = post_query.first()

#     return updated_post_db

# @app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
# def create_user(user: schemas.UserCreate, db:Session=Depends(get_db)):
#     # hash the pass


#     hashed_pass = utils.hash(password=user.password)
#     user.password = hashed_pass
#         # Check whether email already exists
#     existing_user = db.query(models.User).filter(
#         models.User.email == user.email
#     ).first()

#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="Email already registered"
#         )
#     user_data = user.model_dump()
#     user_data["password"] = hashed_pass
#     new_user = models.User(**user_data)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user

# @app.get("/users/{id}",response_model = schemas.UserOut)
# def get_user(id:int,db:Session=Depends(get_db)):
#     user  = db.query(models.User).filter(models.User.id==id).first()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"User with ID : {id} does not exist")
#     return user
