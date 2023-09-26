"""
Kadir Ersoy
Internship Project
Auth Router
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import crud
import schemas
from database.db import get_db
from utils import google, auth

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.get("/google/")
def register_user():
    """Redirects user to google login page"""
    return RedirectResponse(url=google.get_google_auth_url())


# Get user data from identity provider using the code
# Save user data in database,
# Create a JWT token and return it to user,
# token expiration can be same as identity providers token expiration
@router.get("/google/callback")
def oauth2callback(state, code, database: Session = Depends(get_db)):
    """Get user data from identity provider using the code"""
    # Confirm state
    if state != google.STATE:
        raise HTTPException(status_code=401, detail="Invalid state")

    # Get user data from identity provider
    credentials = google.get_credentials(code)
    user_data, exp = google.get_user_data_from_id_token(credentials)

    # Create user
    user = crud.user.get_user_by_email(database, email=user_data["email"])
    if not user:
        user = crud.user.create_user(database, schemas.UserBase(**user_data))

    # Create token
    token = auth.create_access_token(data={"sub": user.email}, expire=exp)
    access_token = {"access_token": token, "token_type": "bearer"}
    return access_token
