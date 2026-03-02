from app import oauth2
from .. import models, schemas
from fastapi import Depends, FastAPI, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import select, delete, update, func

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)

# Get all posts
@router.get("/",response_model=List[schemas.PostWithVotes])
def get_posts(
    db: Session = Depends(get_db),
    token_data = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    stmt = (
        select(
            models.Post,
            func.count(models.Vote.post_id).label("votes")
        )
        .join(
            models.Vote,
            models.Vote.post_id == models.Post.id,
            isouter=True
        )
        .where(models.Post.title.contains(search))
        .group_by(models.Post.id)
        .limit(limit)
        .offset(skip)
    )

    results = db.execute(stmt).all()

    return results
    



# Create new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Post_Response)
def create_post(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db),
    token_data = Depends(oauth2.get_current_user)
):
    new_post = models.Post(owner_id = token_data.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Get single post
@router.get("/{id}", response_model=schemas.PostWithVotes)
def get_post(
    id: int, 
    db: Session = Depends(get_db), 
    token_data = Depends(oauth2.get_current_user)
):
    
    stmt = (
        select(
            models.Post,
            func.count(models.Vote.post_id).label("votes")
        )
        .join(
            models.Vote,
            models.Vote.post_id == models.Post.id,
            isouter=True
        )
        .where(models.Post.id == id)
        .group_by(models.Post.id)
    )
    result = db.execute(stmt).one_or_none()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    
    
    return result
    


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    token_data = Depends(oauth2.get_current_user)
):
    # 1️⃣ Fetch post
    stmt = select(models.Post).where(models.Post.id == id)
    post = db.execute(stmt).scalar_one_or_none()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
 
    # 2️⃣ Check ownership
    if post.owner_id != token_data.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )

    # 3️⃣ Delete post
    delete_stmt = delete(models.Post).where(models.Post.id == id)
    db.execute(delete_stmt)
    db.commit()

# Update post
@router.put("/{id}", response_model=schemas.Post_Response)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db), 
    token_data = Depends(oauth2.get_current_user)
):

    # 1️⃣ Fetch post
    stmt = select(models.Post).where(models.Post.id == id)
    post = db.execute(stmt).scalar_one_or_none()
    
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    
    # 2️⃣ Ownership check
    if post.owner_id != token_data.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post"
        )
    
    # 3️⃣ Update post
    update_stmt = (
        update(models.Post)
        .where(models.Post.id == id)
        .values(**updated_post.model_dump())
        .returning(models.Post)
    )

    result = db.execute(update_stmt).scalar_one()
    db.commit()

    return result