from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List

from sqlalchemy.orm import Session
import models, schemas, utils
from database import get_db


router = APIRouter()


@router.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):

    # cursor.execute("""
    #     SELECT *
    #     FROM posts
    # """)
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()

    return posts


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):

    # Raw SQL approach starts
    # cursor.execute("""
    #     INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING * 
    # """, (post.title, post.content, post.published))
    
    # new_post = cursor.fetchone()
    # conn.commit()
    # Raw SQL approach ends

    # ORM approach
    # first map the fields
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    # But this is not a good approach because, if we have 50 fields we need to do this for 50 fields)
    # So better approach is to use pydantic model to convert to dict and then unpacking the dict
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()

    db.refresh(new_post)

    return new_post

# This need to come first before /posts/{id} because fastapi matches the first similar occurance
# @app.get("/posts/latest")
# def get_latest_post():
#     return {"detail": "this is the latest post"}

@router.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    
    # Raw SQL approach
    # cursor.execute("""
    #     SELECT *
    #     FROM posts
    #     WHERE id = %s
    # """, (str(id),))

    # post = cursor.fetchone()

    # SQLALCHEMY or ORM approach
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""
    #     DELETE FROM posts
    #     WHERE id=%s RETURNING *
    # """, (str(id),))

    # deleted_post = cursor.fetchone()

    # conn.commit()

    # This is only just query
    post = db.query(models.Post).filter(models.Post.id == id)

    # for executing the query we need to add all() or first()

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute("""
    #     UPDATE posts
    #     SET title = %s, content = %s, is_published = %s 
    #     WHERE id = %s 
    #     RETURNING *
    # """, (post.title, post.content, post.published, str(id)))

    # updated_post = cursor.fetchone()

    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    # post_query.update({
    #     'title': 'updated title',
    #     'content': 'this is updated content'
    # }, synchronize_session=False)

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    
    return post_query.first()



# USER FUNCTIONALITIES
@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.get("/users/{id}", response_model=schemas.UserGet)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    print(id, user)

    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found!")

    return user