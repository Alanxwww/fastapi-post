from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, schema, oauth2
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix = "/posts",
    tags=["Posts"]
)

# @router.get("/", response_model=list[schema.Post]) 
@router.get("/", response_model=list[schema.PostOut]) 
def get_posts(
    db: Session = Depends(get_db),
    curent_user: dict = Depends(oauth2.get_current_user),
    limit: int = 5,
    skip: int = 0,
    search: Optional[str] = ""
):
    # cursor.execute(
    #     """SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(search))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # ) 
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes_count"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.ilike(f"%{search}%"))
        .order_by(models.Post.id)
        .limit(limit)
        .offset(skip)
        .all()
    )
    
    return [{"post": post, "votes": votes} for post, votes in posts]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(
    post: schema.PostCreate, 
    curent_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    
    # cursor.execute(
    #     """
    #     INSERT INTO posts (title, content, published)
    #     VALUES (%s, %s, %s) 
    #     RETURNING *;
    #     """,
    #     (post.title, post.content, post.published)
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(get_current_user)
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # print(curent_user.id)
    # print(curent_user.email)
    new_post = models.Post(owner_id=curent_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schema.PostOut)
def get_post(
    id: int, 
    get_current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    # cursor.execute(
    #     """
    #     SELECT * FROM posts WHERE id = %s
    #     """,
    #     (id,) # return tuple
    # )
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()  # from models import Post
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes_count"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first() 
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id:{id} was not found")
    
    post, votes = post

    return {"post": post, "votes": votes}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    curent_user: int = Depends(oauth2.get_current_user)
):
    # cursor.execute(
    #     """
    #     DELETE FROM posts WHERE id = %s RETURNING *
    #     """,
    #     (id,)
    # )
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exist"
        )
    
    if deleted_post.first().owner_id != curent_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to perform requested action"
        )
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schema.Post)
def update_post(
    id: int, 
    post: schema.PostCreate,
    db: Session = Depends(get_db),
    curent_user: int = Depends(oauth2.get_current_user)
    ):
    # cursor.execute(
    #     """
    #     UPDATE posts
    #     set title = %s, content = %s, published = %s
    #     WHERE id = %s RETURNING *
    #     """,
    #     (post.title, post.content, post.published, id)
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # post_to_update = post_query.first()
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    if post_query.first().owner_id != curent_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to perform requested action"
        )
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    updated_post = post_query.first()
    return updated_post

# def find_post(id: int):
#     for post in my_posts:
#         if post["id"] == id:
#             return post

# def find_index_post(id: int):
#     for i, post in enumerate(my_posts):
#         if post["id"] == id:
#             return i