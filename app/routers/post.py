from fastapi import FastAPI,Request,Response,status,HTTPException, Depends,APIRouter
from ..database import get_db
from  .. import models,schemas,utils
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional,List
from sqlalchemy.orm import Session
from app.routers.oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)


  
@router.get("/",response_model=List[schemas.Post])
def get_conncetion(db:Session = Depends(get_db)):

    post = db.query(models.Post).all()
    return post 

 

@router.post("/",status_code=status.HTTP_201_CREATED,
             response_model=schemas.Post) 
def create_posts(new_post:schemas.PostCreate,
                 db:Session = Depends(get_db),
                current_user:int = Depends(get_current_user)): #'''However, there is one important thing: In Pydantic V2, .dict() is deprecated. You should use .model_dump() instead'''
    # new_post = models.Post(title = new_post.title, content=new_post.content) ## it is is inefficient. Use Packing and unpackig the dict.
    print(current_user.email)
    new_post = models.Post(**new_post.model_dump())  ## we packed the dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}",response_model=schemas.Post)
def get_posts(id:int,db:Session = Depends(get_db),current_user:int = Depends(get_current_user)):

    post = db.query(models.Post).filter(models.Post.id==id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    print(type(post))

    return post


@router.delete("/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),current_user:int = Depends(get_current_user)):

    post = db.query(models.Post).filter(models.Post.id==id).first()
    
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} does not exist")
   
    db.delete(post)
    db.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user:int = Depends(get_current_user)
):

    post_query = db.query(models.Post).filter(
        models.Post.id == id
    )

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    post_query.update(
        updated_post.model_dump(),
        synchronize_session="auto"
    )

    db.commit()

    updated_post_db = post_query.first()

    return updated_post_db
