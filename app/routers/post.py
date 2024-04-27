from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import func
from sqlalchemy.orm import Session
import time
from .. import models, schemas, oauth2
from ..database import get_db
# from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts'] 
)

# @router.get("/")
# def read_root():
#     return {"message": "welcome to my api"}

# # Regular SQL
# @router.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts """)
#     posts = cursor.fetchall()
#     return {"data": posts}

# # SQLALCHEMY ORM
# @router.get("/", response_model=List[schemas.Post])
# def get_post(db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    
#     posts = db.query(models.Post).all()
    
#     # #For a specific user posts
#     # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
   
#     print(posts)
#     return posts


# # SQLALCHEMY ORM
# # With limit and skip - pagination
# @router.get("/", response_model=List[schemas.Post])
# async def get_post(db: Session = Depends(get_db),  
#              current_user: int = Depends(oauth2.get_current_user),
#              limit: int = 10, skip:int = 0, search: Optional[str] = ""):
    
#     print(limit)
    
#     posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
#     # #For a specific user posts
#     # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

#     print(posts)
#     return posts


# SQLALCHEMY ORM
# With Count Votes
# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):


    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


# # Regular SQL
# @router.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: schemas.Post):
#     # cursor.execute(f"INSERT INTO posts(title, content, published) VALUES 
#     # ({post.title, post.content, post.published})") this is vaunerable to SQL injection
#      cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s)
#                     RETURNING * """, (post.title, post.content, post.published))
#      new_post = cursor.fetchone()
#      conn.commit()
 
#      return {"data": new_post}

# SQLALCHEMY ORM
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    
    # print(**post.dicts())
    # print(**post.model_dump())
    # new_post = models.Post(title= post.title, content=post.content, published=post.published)
    # new_post = models.Post(**post.dict())
    
    new_post = models.Post(owner_id= current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post

# @router.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     print(post)
#     return {"detail": post}


# # Regular SQL
# @router.get("/posts/{id}")
# def get_post(id: int):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'message': f"post with id: {id} was not found"}
#     return {"post_details": post}

# # SQLALCHEMY ORM
# @router.get("/{id}", response_model=schemas.Post)
# def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
#     post = db.query(models.Post).filter(models.Post.id == id).first()
      
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'message': f"post with id: {id} was not found"}
        
#     # only to retrieve own post
#     # if post.owner_id != current_user.id:
#     #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
#     #                             detail="Not authorised to perform requested action")
#     return post


# SQLALCHEMY ORM
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
      
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
        
    # only to retrieve own post
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    #                             detail="Not authorised to perform requested action")
    return post



# # Regular SQL
# @router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
#     deleted_post = cursor.fetchmany()
#     conn.commit()
    
#     print(deleted_post)
#     if   deleted_post == []:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# SQLALCHEMY ORM
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db),  current_user: models.User = Depends(oauth2.get_current_user)):
   
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    print(post_query.count())
    
    post = post_query.first()
    
    if  post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    # user can delete ownn posts
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                             detail="Not authorised to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

# # Regular SQL
# @router.put("/posts/{id}")
# def update_post(id: int, post: schemas.Post):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
#                    (post.title, post.content, post.published, str(id)))
    
#     updated_post = cursor.fetchone()
#     print( updated_post)
    
#     conn.commit()
    
#     if  updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    
#     return {'data': updated_post}

# SQLALCHEMY ORM
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, update_post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
   
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
     
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    # post_query.update({'title': 'hey this is my updated title', 'content': 'this is my updated content'}, synchronize_session=False)
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail="Not authorised to perform requested action")
        
    post_query.update(update_post.dict(), synchronize_session=False)
    # post_query.update(update_post.model_dump(), synchronize_session=False)
    
    db.commit()
    
    return  post_query.first()
