from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database,schemas, models, utils, oauth2
from sqlalchemy import select
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post("/login",response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    stmt = select(models.User).where(models.User.email == user_credentials.username)
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credencials"
        )
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credencials"
        )
    
    access_token = oauth2.create_access_token(data = {"user_id":user.id})

    return {"access_token":access_token, "token_type":"bearer"}