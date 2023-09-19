"""
Kadir Ersoy
Internship Project
Auth Utils
"""
import os
from typing import Annotated
from datetime import datetime
from jose import JWTError, jwt

from fastapi import HTTPException, Depends, status
from fastapi.security.http import HTTPBearer
from sqlalchemy.orm import Session

from database.db import get_db
import crud

oauth2_scheme = HTTPBearer()

SECRET_KEY = os.environ.get("SECRET_KEY") or None
ALGORITHM = "HS256"

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(data: dict, expire: datetime = None):
    """Create access token"""
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """Decode access token"""
    try:
        # token = Authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as exc:
        raise credentials_exception from exc


def validate_token(token: Annotated[str, HTTPBearer] = Depends(oauth2_scheme)):
    """Validate token"""
    payload = decode_access_token(token.credentials)
    email: str = payload.get("sub")
    exp = payload.get("exp")
    if email == "admin":
        return email
    if email is None:
        raise credentials_exception
    if exp is None:
        raise credentials_exception
    if datetime.utcnow() > datetime.fromtimestamp(exp):
        raise credentials_exception
    return email


def get_current_user(
    email: str = Depends(validate_token), database: Session = Depends(get_db)
):
    """Get current user"""
    user = crud.user.get_user_by_email(database, email=email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
