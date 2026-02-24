from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Dict, Any
from ...database import get_session  # Import from root src directory
from ...models.user import User
from ...services.auth import AuthService
from ...middleware.jwt import JWTBearer, create_access_token, decode_access_token
from pydantic import BaseModel
from datetime import timedelta
import uuid

router = APIRouter()


class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: Dict[str, Any]


class UserProfile(BaseModel):
    id: str
    email: str


from sqlmodel import select

@router.post("/signup", response_model=TokenResponse)
def signup(user_create: UserCreate, session: Session = Depends(get_session)):
    # Check if user already exists
    existing_user_statement = select(User).where(User.email == user_create.email)
    existing_user = session.exec(existing_user_statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )

    # Create new user
    hashed_password = AuthService.get_password_hash(user_create.password)
    user = User(
        email=user_create.email,
        password_hash=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Create access token
    access_token = AuthService.create_access_token_for_user(user)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": str(user.id),
            "email": user.email
        }
    )


@router.post("/login", response_model=TokenResponse)
def login(user_login: UserLogin, session: Session = Depends(get_session)):
    user = AuthService.authenticate_user(
        session, user_login.email, user_login.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = AuthService.create_access_token_for_user(user)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": str(user.id),
            "email": user.email
        }
    )


# Profile endpoint to get user information using JWT validation
@router.get("/user/profile", response_model=UserProfile, dependencies=[Depends(JWTBearer())])
def get_user_profile(request):
    """Get the current user's profile information"""
    user_id = request.state.user.user_id
    email = request.state.user.email

    return UserProfile(
        id=user_id,
        email=email
    )


# Additional endpoints to match frontend expectations
@router.post("/sign-up", response_model=TokenResponse)
def sign_up(user_create: UserCreate, session: Session = Depends(get_session)):
    """Alternative endpoint name that matches frontend expectations"""
    return signup(user_create, session)


@router.post("/sign-in", response_model=TokenResponse)
def sign_in(user_login: UserLogin, session: Session = Depends(get_session)):
    """Alternative endpoint name that matches frontend expectations"""
    return login(user_login, session)


@router.post("/logout")
def logout():
    # For JWT tokens, logout is typically handled client-side by removing the token
    # This endpoint can be used to invalidate tokens on the server if needed
    return {"message": "Logged out successfully"}