"""User service for database operations."""
import uuid
from datetime import datetime
from typing import Optional

import bcrypt
from sqlalchemy.orm import Session

from app.models.db import User


def create_user(db: Session, email: str, password_hash: str, nickname: Optional[str] = None) -> User:
    """Create a new user."""
    user = User(
        id=str(uuid.uuid4()),
        email=email,
        password_hash=password_hash,
        nickname=nickname or email.split("@")[0],
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), password_hash.encode('utf-8'))


def hash_password(password: str) -> str:
    """Hash a password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')