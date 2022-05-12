from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2, schemas, models, utils

router = APIRouter(
    tags=["Authentication"]
)


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # searches database for entry based on provided email
    # OAuth2Password Request form returns {username: " ", password: " "} as a dict, there is no field for email. Will use "username" as an alias for email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # checks to see if email is in database
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # passes users password attempt AND password stored in the database to the verify function in utils.py
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # create access token with the given payload
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}