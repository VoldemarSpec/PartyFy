import jwt
from datetime import datetime, timedelta, timezone
import os
import bcrypt
from fastapi import HTTPException, status
from jwt import ExpiredSignatureError, InvalidTokenError
from dotenv import load_dotenv

load_dotenv(".env.auth")

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
GUEST_ACCESS_TOKEN_EXPIRE_MINUTES = 120
def create_access_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode({"sub": str(user_id),
                               "exp": expire,
                               "type": "access"}, SECRET_KEY, algorithm="HS256")
    return access_token


def create_guest_access_token(party_uuid: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=GUEST_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode({"sub": "guest",
                               "exp": expire,
                               "type": "access",
                               "party_uuid": party_uuid}, SECRET_KEY, algorithm="HS256"
                                )
    return access_token



def create_refresh_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = jwt.encode({"sub": str(user_id),
                               "exp": expire,
                                "type": "refresh"}, SECRET_KEY, algorithm="HS256")
    return refresh_token



def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"
        ])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    return payload


def verify_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"],
        )
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    return payload



def hash_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))