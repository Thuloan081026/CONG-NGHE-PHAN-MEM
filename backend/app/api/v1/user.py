from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...core.database import get_db
from ...schemas.user_schema import UserOut, PasswordChange, UserCreate
from ...repositories import user_repo
from ...services import user_service
from ...core.deps import get_current_user, require_roles

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserOut])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    users = user_repo.list_users(db, skip=skip, limit=limit)
    return users


@router.post("/change-password")
def change_password(payload: PasswordChange, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        user_service.change_password(db, current_user, payload.old_password, payload.new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Password changed"}


@router.post("/import-csv")
def import_csv(file_path: str, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    # For simplicity the endpoint accepts a server-side file path to a CSV.
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
