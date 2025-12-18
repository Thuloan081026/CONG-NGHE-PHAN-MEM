"""
Settings API - Admin only
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from ...core.database import get_db
from ...core.deps import get_current_user, require_roles
from ...models.user import User
from ...services.settings_service import SettingsService
from ...schemas.settings_schema import (
    SettingCreate, SettingUpdate, SettingOut, GeminiKeyUpdate
)

router = APIRouter(prefix="/settings", tags=["Settings (Admin Only)"])


@router.get("/", response_model=Dict[str, Any])
def get_all_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    """
    Get all system settings (Admin only)
    
    **Encrypted values will show as ***ENCRYPTED*****
    """
    settings = SettingsService.get_all_settings(db, include_encrypted=False)
    return settings


@router.get("/{key}")
def get_setting(
    key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    """Get specific setting by key (Admin only)"""
    value = SettingsService.get_setting(db, key)
    
    if value is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    
    return {"key": key, "value": value}


@router.post("/")
def create_setting(
    setting: SettingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    """Create new setting (Admin only)"""
    result = SettingsService.set_setting(
        db,
        setting.key,
        setting.value,
        setting.description,
        setting.encrypt,
        current_user.id
    )
    
    return {
        "message": "Setting created successfully",
        "key": result.key,
        "encrypted": result.is_encrypted
    }


@router.put("/{key}")
def update_setting(
    key: str,
    setting: SettingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    """Update existing setting (Admin only)"""
    result = SettingsService.set_setting(
        db,
        key,
        setting.value,
        setting.description,
        user_id=current_user.id
    )
    
    return {
        "message": "Setting updated successfully",
        "key": result.key
    }


@router.put("/gemini/api-key")
def update_gemini_api_key(
    data: GeminiKeyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    """
    Update Gemini API Key (Admin only)
    
    **API key will be encrypted in database**
    """
    success = SettingsService.update_gemini_api_key(
        db, data.api_key, current_user.id
    )
    
    if success:
        return {
            "message": "Gemini API key updated successfully",
            "encrypted": True,
            "updated_by": current_user.email
        }
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to update API key"
        )


@router.get("/gemini/test")
def test_gemini_connection(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    """Test Gemini API connection (Admin only)"""
    try:
        import google.generativeai as genai
        
        api_key = SettingsService.get_gemini_api_key(db)
        
        if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
            return {
                "status": "not_configured",
                "message": "Gemini API key not set",
                "api_key_set": False
            }
        
        # Test connection
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Say 'Hello' in one word")
        
        return {
            "status": "success",
            "message": "Gemini API is working",
            "api_key_set": True,
            "test_response": response.text[:50]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "api_key_set": True
        }
