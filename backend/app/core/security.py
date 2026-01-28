from datetime import datetime, timedelta
from typing import Optional
import hashlib

from passlib.context import CryptContext
import jwt

from .config import settings

# Use argon2 for better security, fallback to bcrypt then sha256
pwd_context = None
try:
    pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
except Exception:
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    except:
        try:
            pwd_context = CryptContext(schemes=["plaintext"], deprecated="auto")
        except:
            pass


def get_password_hash(password: str) -> str:
    """Hash password - ưu tiên argon2, fallback sha256"""
    # Nếu password đã là hash sha256 (64 ký tự hex), trả về luôn
    if len(password) == 64 and all(c in '0123456789abcdef' for c in password.lower()):
        return password
    
    # Try to use passlib (argon2 or bcrypt)
    if pwd_context:
        try:
            return pwd_context.hash(password)
        except:
            pass
    
    # Fallback to sha256
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password - hỗ trợ argon2, bcrypt, sha256"""
    # Try passlib first (supports argon2, bcrypt)
    if pwd_context:
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except:
            pass
    
    # Nếu hash là sha256 (64 ký tự hex), dùng sha256 để verify
    if len(hashed_password) == 64 and all(c in '0123456789abcdef' for c in hashed_password.lower()):
        sha256_hash = hashlib.sha256(plain_password.encode()).hexdigest()
        return sha256_hash == hashed_password
    
    # Last resort - try sha256
    try:
        sha256_hash = hashlib.sha256(plain_password.encode()).hexdigest()
        return sha256_hash == hashed_password
    except:
        return False
        return False


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"sub": subject, "exp": expire, "type": "access"}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    payload = {"sub": subject, "exp": expire, "type": "refresh"}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

