from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...core.database import get_db
from ...schemas.user_schema import UserOut, UserListOut, UserCreate, UserUpdate, PasswordChange
from ...repositories import user_repo
from ...services import user_service
from ...core.deps import get_current_user, require_roles

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    """Create a new user (Admin only)"""
    try:
        user = user_service.register_user(db, user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user


@router.get("/", response_model=List[UserListOut])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    """List all users (Admin only)"""
    users = user_repo.list_users(db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=UserOut)
def get_me(current_user=Depends(get_current_user)):
    """Get current authenticated user info"""
    # Convert SQLAlchemy model to dict for proper serialization
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": bool(current_user.is_active),
    }


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Get user by ID (Admin or self)"""
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Update user (Admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    try:
        user = user_service.update_user_info(db, user_id, user_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return user


@router.patch("/{user_id}/lock", response_model=UserOut)
def lock_user(user_id: int, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    """Lock user account (Admin only)"""
    try:
        user = user_service.lock_user_account(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return user


@router.patch("/{user_id}/unlock", response_model=UserOut)
def unlock_user(user_id: int, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    """Unlock user account (Admin only)"""
    try:
        user = user_service.unlock_user_account(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return user


@router.post("/change-password")
def change_password(payload: PasswordChange, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Change password (Authenticated users)"""
    try:
        user_service.change_password(db, current_user, payload.old_password, payload.new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Password changed"}


@router.post("/import-csv")
def import_csv(file_path: str, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    """Import users from CSV file (Admin only)"""
    import csv

    rows = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for r in reader:
                rows.append(r)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    created = user_service.import_users_from_list(db, rows)
    return {"created": len(created)}
