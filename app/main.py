from fastapi import FastAPI,Request,Response,status,HTTPException
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

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

app = FastAPI()

class post(BaseModel):
    title: str
    content: str
    published:Optional[str] = None
    rating:Optional[int] = None


while True:
    try:
        conn = psycopg2.connect(host = DB_HOST,database = DB_NAME,
                                user=DB_USER, password=DB_PASSWORD, port = int(DB_PORT), 
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("daabase connection successfull")
        break

    except Exception as error:
        print("db connection failed")
        print(f"Db error {error}")
        time.sleep(2)


my_posts = [{"title":"post-1","content":"This is the content about post-1","id":1},
            {"title":"post-2","content":"this is the content about post-2","id":2}]

def find_posts(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i   
 
 
@app.get("/")
def home():
    return {"message": "Welcome to FastAPI"}

@app.get("/posts")
def about(): 
    cursor.execute("""select * from post""")
    posts=cursor.fetchall()
    print(posts)
    return {"posts":posts}

@app.post("/createposts",status_code=status.HTTP_201_CREATED) 
def create_posts(new_post:post): #'''However, there is one important thing: In Pydantic V2, .dict() is deprecated. You should use .model_dump() instead'''
    cursor.execute("""INSERT INTO post (title,content,published) VALUES (%s, %s, %s) RETURNING * """,
                   (new_post.title,new_post.content,new_post.published))
    new_post = cursor.fetchone()

    conn.commit()

    return {"data" :new_post}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"details": post}

@app.get("/posts/{id}")
def get_posts(id:str):
    cursor.execute("""SELECT * FROM post WHERE id = %s""", (int(id), ))
    post = cursor.fetchone()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f'posts with id: {id} was not found'}
    return {"post_details" : post} 


@app.delete("/posts/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int):

    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING * """, (int(id),))
    deleted_post = cursor.fetchone()
    conn.commit()


    if deleted_post ==None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} does not exist")



    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post:post):
    cursor.execute("""UPDATE post SET title = %s, content = %s, published= %s WHERE id=%s RETURNING *""",
                   (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return {'message':updated_post}
