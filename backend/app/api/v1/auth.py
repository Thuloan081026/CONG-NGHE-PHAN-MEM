from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core import security
from ...core.deps import get_current_user
from ...schemas.user_schema import UserCreate, Token, PasswordChange, UserOut
from ...services import user_service
from ...repositories import user_repo

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        user = user_service.register_user(db, user_in)
        db.commit()  # Manual commit
        return f"User {user.email} created successfully with ID {user.id}"
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    # Remove db.close() - let dependency injection handle it


@router.post("/login", response_model=Token)
def login(form_data: UserCreate, db: Session = Depends(get_db)):
    # reuse UserCreate for email/password payload here
    user = user_service.authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = security.create_access_token(subject=str(user.id))
    refresh_token = security.create_refresh_token(subject=str(user.id))
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh", response_model=Token)
def refresh(token: dict, db: Session = Depends(get_db)):
    # token: {"refresh_token": "..."}
    refresh_token = token.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Missing refresh token")
    try:
        data = security.decode_token(refresh_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    if data.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Not a refresh token")
    user = user_repo.get_user(db, int(data.get("sub")))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    access_token = security.create_access_token(subject=str(user.id))
    refresh_token = security.create_refresh_token(subject=str(user.id))
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/change-password")
def change_password(payload: PasswordChange, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        user_service.change_password(db, current_user, payload.old_password, payload.new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Password changed"}
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from ...core.database import get_db
from ...core import security
from ...schemas.user_schema import UserCreate, Token, PasswordChange, UserOut
from ...services import user_service
from ...repositories import user_repo

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
	try:
		user = user_service.register_user(db, user_in)
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	return user

@router.post("/login", response_model=Token)
def login(form_data: UserCreate, db: Session = Depends(get_db)):
	# reuse UserCreate for email/password payload here
	user = user_service.authenticate_user(db, form_data.email, form_data.password)
	if not user:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
	access_token = security.create_access_token(subject=str(user.id), expires_delta=timedelta(minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES))
	refresh_token = security.create_refresh_token(subject=str(user.id))
	return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/refresh", response_model=Token)
def refresh(token: dict, db: Session = Depends(get_db)):
	# token: {"refresh_token": "..."}
	refresh_token = token.get("refresh_token")
	if not refresh_token:
		raise HTTPException(status_code=400, detail="Missing refresh token")
	try:
		data = security.decode_token(refresh_token)
	except Exception:
		raise HTTPException(status_code=401, detail="Invalid token")
	if data.get("type") != "refresh":
		raise HTTPException(status_code=401, detail="Not a refresh token")
	user = user_repo.get_user(db, int(data.get("sub")))
	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	access_token = security.create_access_token(subject=str(user.id))
	refresh_token = security.create_refresh_token(subject=str(user.id))
	return {"access_token": access_token, "refresh_token": refresh_token}

def get_current_user(db: Session = Depends(get_db), token: str = Depends(None)):
	# Simplified dependency placeholder for further extension
	raise HTTPException(status_code=501, detail="Not implemented: use dependency in real app")

@router.post("/change-password")
def change_password(payload: PasswordChange, db: Session = Depends(get_db)):
	# For demo: expects payload contains email as old_password field? In real app get current user from token
	raise HTTPException(status_code=501, detail="Use /users/change-password with authenticated user in real app")
