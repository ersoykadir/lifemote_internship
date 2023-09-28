"""
Kadir Ersoy
Internship Project
Auth Utils
"""
import os
from typing import Annotated, Dict, Any
from datetime import datetime
from jose import JWTError, jwt

from fastapi import HTTPException, Depends, status
from fastapi.security.http import HTTPBearer
from sqlalchemy.orm import Session

from server.database.db import get_db
from server.crud import user_instance

oauth2_scheme = HTTPBearer()

SECRET_KEY = os.environ.get("SECRET_KEY") or None
ALGORITHM = "HS256"

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(data: Dict[str, Any], expire: datetime):
    """Create access token"""
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """Decode access token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as exc:
        # cr = credentials_exception
        # cr.detail = f"Could not validate credentials,
        # token is not valid, {token}"
        # Log this error
        raise credentials_exception from exc


def validate_token(token: Annotated[Any, HTTPBearer] = Depends(oauth2_scheme)):
    """Validate token"""
    payload = decode_access_token(token.credentials)
    email: str = payload.get("sub")
    exp = payload.get("exp")
    if email == "admin":
        return email
    if email is None:
        # cr = credentials_exception
        # cr.detail = "Could not validate credentials, email is None"
        # Log this error
        raise credentials_exception
    if exp is None:
        # cr = credentials_exception
        # cr.detail = "Could not validate credentials, exp is None"
        # Log this error
        raise credentials_exception
    if datetime.utcnow() > datetime.fromtimestamp(exp):
        # cr = credentials_exception
        # cr.detail = "Could not validate credentials, token expired"
        # Log this error
        raise credentials_exception
    return email


def get_current_user(
    email: str = Depends(validate_token), database: Session = Depends(get_db)
):
    """Get current user"""
    current_user = user_instance.get_user_by_email(database, email=email)
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return current_user
