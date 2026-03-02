from .. import models, utils, schemas
from fastapi import Depends, FastAPI, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import select


router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db : Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    stmt = select(models.User).where(models.User.id == id)
    user = db.execute(stmt).scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"User with id: {id} not found"
        )
    
    return user