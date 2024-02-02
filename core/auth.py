from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import config
from models import models
from schema import schemas
from auth.hash import Hash
from auth.token import create_access_token

router = APIRouter(prefix="/login", tags=["Authentication"],)


@router.post("/")
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(config.get_db),
):
    """
    Login user

    Args:
        request (OAuth2PasswordRequestForm, optional): OAuth2PasswordRequestForm.
        db (Session, optional): Session. Defaults to Depends(config.get_db).

    Raises:
        HTTPException: 401 Unauthorized
        HTTPException: 404 Not Found

    Returns:
        Hash: Hash
    """
    user: schemas.User = db.query(models.User).filter(
        models.User.email == request.username
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
        )

    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password"
        )

    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email})

    # generate JWT token and return
    return {"access_token": access_token, "token_type": "bearer"}
