"""Authentication API routes."""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr, field_validator

from app.core.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# Models
class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    """User registration request."""
    email: EmailStr
    password: str
    nickname: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password is at least 8 characters."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserResponse(BaseModel):
    """User response."""
    id: str
    email: EmailStr
    nickname: Optional[str]
    is_premium: bool = False
    created_at: datetime


class UserInDB(UserResponse):
    """User with password hash."""
    password_hash: str


# Helpers
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Mock user for now - will get from DB
    return UserResponse(
        id=user_id,
        email="user@example.com",
        nickname=None,
        is_premium=False,
        created_at=datetime.utcnow(),
    )


# Routes
@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    """Register a new user."""
    # TODO: Implement actual registration with DB
    # For now, return mock user
    return UserResponse(
        id="mock-user-id",
        email=user.email,
        nickname=user.nickname,
        is_premium=False,
        created_at=datetime.utcnow(),
    )


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token."""
    # TODO: Implement actual login with DB
    # For now, return mock token
    access_token = create_access_token(
        data={"sub": "mock-user-id"},
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """Get current user info."""
    return current_user