from fastapi import Depends, status, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from app import models, schemas, oauth2, database
from fastapi.routing import APIRouter

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    token_data = Depends(oauth2.get_current_user)
):
    #  Check if post exists
    post_stmt = select(models.Post).where(models.Post.id == vote.post_id)
    post = db.execute(post_stmt).scalar_one_or_none()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist"
        )
    

    #  Check if vote already exists (composite key)
    vote_stmt = select(models.Vote).where(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == token_data.id
    )
    existing_vote = db.execute(vote_stmt).scalar_one_or_none()

    # Add vote
    if vote.dir == 1:
        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User has already voted on this post"
            )

        new_vote = models.Vote(
            post_id=vote.post_id,
            user_id=token_data.id
        )
        db.add(new_vote)
        db.commit()

        return {"message": "Successfully added vote"}

    # Remove vote
    else:
        if not existing_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist"
            )

        delete_stmt = delete(models.Vote).where(
            models.Vote.post_id == vote.post_id,
            models.Vote.user_id == token_data.id
        )
        db.execute(delete_stmt)
        db.commit()

        return {"message": "Successfully deleted vote"}