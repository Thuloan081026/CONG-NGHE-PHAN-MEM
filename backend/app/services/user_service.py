from typing import Optional, List
from sqlalchemy.orm import Session

from ..schemas.user_schema import UserCreate, UserUpdate
from ..repositories import user_repo
from ..core.security import get_password_hash, verify_password


def register_user(db: Session, user_in: UserCreate):
    existing = user_repo.get_user_by_email(db, user_in.email)
    if existing:
        raise ValueError("Email already registered")
    try:
        hashed = get_password_hash(user_in.password)
        return user_repo.create_user(db, email=user_in.email, full_name=user_in.full_name or "", hashed_password=hashed, role=user_in.role)
    except Exception as e:
        raise


def authenticate_user(db: Session, email: str, password: str):
    user = user_repo.get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def change_password(db: Session, user, old_password: str, new_password: str):
    if not verify_password(old_password, user.hashed_password):
        raise ValueError("Old password incorrect")
    new_hashed = get_password_hash(new_password)
    return user_repo.update_password(db, user, new_hashed)


def import_users_from_list(db: Session, rows: List[dict]):
    # rows expected to have keys: email, full_name, password, role
    to_create = []
    for r in rows:
        to_create.append({
            "email": r["email"],
            "full_name": r.get("full_name", ""),
            "hashed_password": get_password_hash(r.get("password", "123456")),
            "role": r.get("role", "student"),
        })
    return user_repo.create_users_bulk(db, to_create)


def update_user_info(db: Session, user_id: int, user_update: UserUpdate):
    user = user_repo.get_user(db, user_id)
    if not user:
        raise ValueError("User not found")
    return user_repo.update_user(db, user, **user_update.dict(exclude_unset=True))


def lock_user_account(db: Session, user_id: int):
    user = user_repo.get_user(db, user_id)
    if not user:
        raise ValueError("User not found")
    return user_repo.lock_user(db, user)


def unlock_user_account(db: Session, user_id: int):
    user = user_repo.get_user(db, user_id)
    if not user:
        raise ValueError("User not found")
    return user_repo.unlock_user(db, user)
