import google.oauth2.credentials
import google_auth_oauthlib.flow
from google.auth import jwt as jwt_google
import json, os
from jose import JWTError
from fastapi import HTTPException, status

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID") or None
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET") or None

if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise Exception("GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET is not set")

STATE = "random_state_value"

client_config = {
    "web": {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uris": [
            "http://127.0.0.1:3000/auth/google/callback",
            "http://localhost:3000/auth/google/callback",
        ],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}

flow = google_auth_oauthlib.flow.Flow.from_client_config(
    client_config,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
)


def get_google_auth_url():
    # Indicate where the API server will redirect the user after the user completes
    flow.redirect_uri = "http://localhost:3000/auth/google/callback"

    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        # access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        # include_granted_scopes='true'
        state=STATE,
        prompt="consent",
    )
    return authorization_url


def get_credentials(code):
    flow.fetch_token(code=code)
    credentials = flow.credentials
    return credentials


def get_user_data_from_id_token(credentials):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials._id_token
        payload = jwt_google.decode(token, verify=False)
        user_data = {
            "name": payload.get("name"),
            "email": payload.get("email"),
        }
        exp = payload.get("exp")
        if not payload.get("email_verified"):
            raise credentials_exception
        if payload.get('email') == 'admin':
            raise credentials_exception
        return user_data, exp
    except JWTError:
        raise credentials_exception
