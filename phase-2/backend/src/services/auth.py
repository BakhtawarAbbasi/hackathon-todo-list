from datetime import timedelta
from typing import Optional
from sqlmodel import Session, select
import bcrypt
from ..models.user import User
from ..middleware.jwt import create_access_token
import warnings

# Suppress the bcrypt version warning
warnings.filterwarnings("ignore", message=".*bcrypt.*__about__.*")

# Using bcrypt directly to avoid passlib version detection issues


class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password"""
        # Truncate password to 72 bytes as bcrypt has this limitation
        truncated_password = plain_password[:72] if len(plain_password) > 72 else plain_password
        password_bytes = truncated_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a plain password, truncating if needed to comply with bcrypt limits"""
        # Truncate password to 72 bytes as bcrypt has this limitation
        truncated_password = password[:72] if len(password) > 72 else password
        password_bytes = truncated_password.encode('utf-8')
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password"""
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()

        if not user:
            return None

        if not AuthService.verify_password(password, user.password_hash):
            return None

        return user

    @staticmethod
    def create_access_token_for_user(user: User) -> str:
        """Create an access token for a user"""
        data = {
            "user_id": str(user.id),
            "email": user.email
        }
        expire = timedelta(days=7)  # 7 days expiration
        return create_access_token(data=data, expires_delta=expire)