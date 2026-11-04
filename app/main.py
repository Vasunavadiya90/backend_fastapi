from fastapi import FastAPI,Request,Response,status,HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from app.database import Base, SessionLocal,engine,get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI()

class post(BaseModel):
    title: str
    content: str
    published:Optional[bool] = None
   
@app.get("/posts")
def get_conncetion(db:Session = Depends(get_db)):

    post = db.query(models.Post).all()
    return {"data": post }

 

@app.post("/createposts",status_code=status.HTTP_201_CREATED) 
def create_posts(new_post:post,db:Session = Depends(get_db) ): #'''However, there is one important thing: In Pydantic V2, .dict() is deprecated. You should use .model_dump() instead'''
    # new_post = models.Post(title = new_post.title, content=new_post.content) ## it is is inefficient. Use Packing and unpackig the dict.
    new_post = models.Post(**new_post.model_dump())  ## we packed the dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data" :new_post}


@app.get("/posts/{id}")
def get_posts(id:str,db:Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id==id).first()
    print(type(post))

    return {"post_details" : post} 


@app.delete("/posts/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id==id).first()
    
    if post ==None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} does not exist")
   
    db.delete(post)
    db.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int,updated_post:post,db:Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_query.update(updated_post.model_dump())
    db.commit()

    return {'message':post_query.first()}
