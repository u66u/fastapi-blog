from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from schema.schemas import TokenData


load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
HASH_ALGO = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", default=60)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Generate JWT token

    Args:
        data (dict): payload
        expires_delta (Optional[timedelta]): token expiration time

    Returns:
        str: JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=HASH_ALGO)


def verify_token(token: str, credentials_exception):
    """
    Verify JWT token

    Args:
        token (str): JWT token
        credentials_exception (Exception): exception to raise if token is invalid

    Raises:
        credentials_exception: if token is invalid
        credentials_exception: if token is expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=HASH_ALGO)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
