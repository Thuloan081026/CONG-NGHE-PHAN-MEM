from sqlalchemy.orm import Session
from typing import List, Optional

from ..models.user import User


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def list_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, *, email: str, full_name: str, hashed_password: str, role: str = "student") -> User:
    user = User(email=email, full_name=full_name, hashed_password=hashed_password, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_password(db: Session, user: User, new_hashed_password: str) -> User:
    user.hashed_password = new_hashed_password
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, **kwargs) -> User:
    for key, value in kwargs.items():
        if hasattr(user, key) and key not in ["id", "hashed_password"]:
            setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def lock_user(db: Session, user: User) -> User:
    user.is_active = False
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def unlock_user(db: Session, user: User) -> User:
    user.is_active = True
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_users_bulk(db: Session, users_data: list) -> List[User]:
    created = []
    for u in users_data:
        user = User(email=u["email"], full_name=u.get("full_name"), hashed_password=u["hashed_password"], role=u.get("role", "student"))
        db.add(user)
        created.append(user)
    db.commit()
    for c in created:
        db.refresh(c)
    return created
