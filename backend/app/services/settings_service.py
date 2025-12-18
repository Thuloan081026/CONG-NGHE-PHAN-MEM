"""
Settings Management Service
"""
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
import os
import base64

from ..models.system_setting import SystemSetting
from ..core.config import settings


class SettingsService:
    """Service for managing system settings"""
    
    # Encryption key (should be in environment variable)
    ENCRYPTION_KEY = base64.urlsafe_b64encode(
        settings.SECRET_KEY.encode()[:32].ljust(32, b'0')
    )
    
    @staticmethod
    def get_setting(db: Session, key: str, default: Any = None) -> Any:
        """Get setting value by key"""
        setting = db.query(SystemSetting).filter(
            SystemSetting.key == key,
            SystemSetting.is_active == True
        ).first()
        
        if not setting:
            return default
        
        value = setting.value
        
        # Decrypt if needed
        if setting.is_encrypted and value:
            try:
                cipher = Fernet(SettingsService.ENCRYPTION_KEY)
                value = cipher.decrypt(value.encode()).decode()
            except Exception:
                return default
        
        return value
    
    @staticmethod
    def set_setting(
        db: Session, 
        key: str, 
        value: str,
        description: Optional[str] = None,
        encrypt: bool = False,
        user_id: Optional[int] = None
    ) -> SystemSetting:
        """Create or update setting"""
        setting = db.query(SystemSetting).filter(
            SystemSetting.key == key
        ).first()
        
        # Encrypt sensitive data
        if encrypt and value:
            cipher = Fernet(SettingsService.ENCRYPTION_KEY)
            value = cipher.encrypt(value.encode()).decode()
        
        if setting:
            # Update existing
            setting.value = value
            if description:
                setting.description = description
            setting.is_encrypted = encrypt
            setting.updated_by = user_id
        else:
            # Create new
            setting = SystemSetting(
                key=key,
                value=value,
                description=description,
                is_encrypted=encrypt,
                updated_by=user_id
            )
            db.add(setting)
        
        db.commit()
        db.refresh(setting)
        return setting
    
    @staticmethod
    def get_gemini_api_key(db: Session) -> str:
        """Get Gemini API key from database or fallback to config"""
        # Try database first
        api_key = SettingsService.get_setting(db, "GEMINI_API_KEY")
        
        # Fallback to config file
        if not api_key:
            api_key = settings.GEMINI_API_KEY
        
        return api_key
    
    @staticmethod
    def update_gemini_api_key(db: Session, api_key: str, user_id: int) -> bool:
        """Update Gemini API key (encrypted)"""
        try:
            SettingsService.set_setting(
                db, 
                "GEMINI_API_KEY", 
                api_key,
                description="Google Gemini AI API Key",
                encrypt=True,
                user_id=user_id
            )
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_all_settings(db: Session, include_encrypted: bool = False) -> Dict[str, Any]:
        """Get all settings"""
        settings_list = db.query(SystemSetting).filter(
            SystemSetting.is_active == True
        ).all()
        
        result = {}
        for setting in settings_list:
            if setting.is_encrypted and not include_encrypted:
                result[setting.key] = "***ENCRYPTED***"
            else:
                result[setting.key] = SettingsService.get_setting(db, setting.key)
        
        return result
