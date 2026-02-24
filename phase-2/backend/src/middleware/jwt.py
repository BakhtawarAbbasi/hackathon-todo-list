from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os

# Get the JWT secret from environment variable - this should match Better Auth's secret
JWT_SECRET = os.getenv("BETTER_AUTH_SECRET", "fallback-secret-key-for-development")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


class TokenData(BaseModel):
    user_id: str
    email: str


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            token = credentials.credentials
            token_data = self.verify_jwt(token)
            if not token_data:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            # Attach user info to request for use in endpoints
            request.state.user = token_data
            return token
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> Optional[TokenData]:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
            user_id: str = payload.get("user_id")
            email: str = payload.get("email")

            # For Better Auth compatibility, also check for other possible fields
            if user_id is None:
                user_id = payload.get("id") or payload.get("sub")
            if email is None:
                email = payload.get("email")

            if user_id is None or email is None:
                return None

            token_data = TokenData(user_id=user_id, email=email)
            return token_data
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:
            return None


# Add any imports needed for the JWT functions
from datetime import datetime, timedelta
import jwt
import os
from typing import Optional
from pydantic import BaseModel

JWT_SECRET = os.getenv("BETTER_AUTH_SECRET", "fallback-secret-key-for-development")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        email: str = payload.get("email")

        # For Better Auth compatibility, also check for other possible fields
        if user_id is None:
            user_id = payload.get("id") or payload.get("sub")
        if email is None:
            email = payload.get("email")

        if user_id is None or email is None:
            return None

        token_data = TokenData(user_id=user_id, email=email)
        return token_data
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None