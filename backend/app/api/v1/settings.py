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


# Specific routes MUST come before generic path parameters
@router.get("/general", response_model=Dict[str, Any])
def get_general_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    """
    Get all general system settings (Admin only)
    Returns settings organized by category
    """
    try:
        settings = SettingsService.get_all_settings(db, include_encrypted=False)
        
        # Organize settings with defaults
        return {
            "currentSemester": settings.get("current_semester", "2"),
            "academicYear": settings.get("academic_year", "2024-2025"),
            "semesterStartDate": settings.get("semester_start_date", "2025-01-06"),
            "semesterEndDate": settings.get("semester_end_date", "2025-05-30"),
            "universityName": settings.get("university_name", "Ho Chi Minh City University of Technology and Education"),
            "universityCode": settings.get("university_code", "HCMUTE"),
            "universityEmail": settings.get("university_email", "info@hcmute.edu.vn"),
            "universityAddress": settings.get("university_address", "01 Vo Van Ngan Street, Thu Duc City, Ho Chi Minh City, Vietnam"),
            "syllabusVersion": settings.get("syllabus_version", "v1.0"),
            "reviewDeadline": int(settings.get("review_deadline", "7")),
            "autoVersioning": settings.get("auto_versioning", "true").lower() == "true",
            "requireHodApproval": settings.get("require_hod_approval", "true").lower() == "true",
            "enableNotifications": settings.get("enable_notifications", "true").lower() == "true",
            "defaultLanguage": settings.get("default_language", "en"),
            "timezone": settings.get("timezone", "Asia/Ho_Chi_Minh"),
            "dateFormat": settings.get("date_format", "DD/MM/YYYY"),
            "pageSize": int(settings.get("page_size", "20"))
        }
    except Exception as e:
        # Return defaults if any error
        return {
            "currentSemester": "2",
            "academicYear": "2024-2025",
            "semesterStartDate": "2025-01-06",
            "semesterEndDate": "2025-05-30",
            "universityName": "Ho Chi Minh City University of Technology and Education",
            "universityCode": "HCMUTE",
            "universityEmail": "info@hcmute.edu.vn",
            "universityAddress": "01 Vo Van Ngan Street, Thu Duc City, Ho Chi Minh City, Vietnam",
            "syllabusVersion": "v1.0",
            "reviewDeadline": 7,
            "autoVersioning": True,
            "requireHodApproval": True,
            "enableNotifications": True,
            "defaultLanguage": "en",
            "timezone": "Asia/Ho_Chi_Minh",
            "dateFormat": "DD/MM/YYYY",
            "pageSize": 20
        }


@router.post("/general")
def save_general_settings(
    settings: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    """
    Save all general system settings (Admin only)
    Accepts a dictionary of settings and saves each one
    """
    try:
        # Map of frontend keys to database keys
        setting_map = {
            "currentSemester": "current_semester",
            "academicYear": "academic_year",
            "semesterStartDate": "semester_start_date",
            "semesterEndDate": "semester_end_date",
            "universityName": "university_name",
            "universityCode": "university_code",
            "universityEmail": "university_email",
            "universityAddress": "university_address",
            "syllabusVersion": "syllabus_version",
            "reviewDeadline": "review_deadline",
            "autoVersioning": "auto_versioning",
            "requireHodApproval": "require_hod_approval",
            "enableNotifications": "enable_notifications",
            "defaultLanguage": "default_language",
            "timezone": "timezone",
            "dateFormat": "date_format",
            "pageSize": "page_size"
        }
        
        saved_count = 0
        for frontend_key, db_key in setting_map.items():
            if frontend_key in settings:
                value = settings[frontend_key]
                # Convert boolean to string for storage
                if isinstance(value, bool):
                    value = "true" if value else "false"
                else:
                    value = str(value)
                
                SettingsService.set_setting(
                    db,
                    db_key,
                    value,
                    description=f"General setting: {frontend_key}",
                    encrypt=False,
                    user_id=current_user.id
                )
                saved_count += 1
        
        return {
            "message": f"Successfully saved {saved_count} settings",
            "saved_count": saved_count,
            "updated_by": current_user.email
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save settings: {str(e)}"
        )


@router.get("/grading", response_model=Dict[str, Any])
def get_grading_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    """
    Get grading scale and assessment settings (Admin only)
    """
    try:
        settings = SettingsService.get_all_settings(db, include_encrypted=False)
        
        return {
            # Assessment weights
            "weightAttendance": float(settings.get("weight_attendance", "10")),
            "weightAssignments": float(settings.get("weight_assignments", "20")),
            "weightMidterm": float(settings.get("weight_midterm", "30")),
            "weightFinal": float(settings.get("weight_final", "40")),
            "weightProject": float(settings.get("weight_project", "0")),
            "weightLab": float(settings.get("weight_lab", "0")),
            
            # Pass/fail criteria
            "minPassScore": float(settings.get("min_pass_score", "50")),
            "minFinalScore": float(settings.get("min_final_score", "40")),
            "minAttendance": float(settings.get("min_attendance", "80")),
            "minGradePoint": float(settings.get("min_grade_point", "2.0")),
            
            # Options
            "requireAllComponents": settings.get("require_all_components", "true").lower() == "true",
            "allowRetake": settings.get("allow_retake", "true").lower() == "true",
            "roundGrades": settings.get("round_grades", "true").lower() == "true"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load grading settings: {str(e)}"
        )


@router.post("/grading")
def save_grading_settings(
    settings: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    """
    Save grading scale and assessment settings (Admin only)
    """
    try:
        setting_map = {
            "weightAttendance": "weight_attendance",
            "weightAssignments": "weight_assignments",
            "weightMidterm": "weight_midterm",
            "weightFinal": "weight_final",
            "weightProject": "weight_project",
            "weightLab": "weight_lab",
            "minPassScore": "min_pass_score",
            "minFinalScore": "min_final_score",
            "minAttendance": "min_attendance",
            "minGradePoint": "min_grade_point",
            "requireAllComponents": "require_all_components",
            "allowRetake": "allow_retake",
            "roundGrades": "round_grades"
        }
        
        saved_count = 0
        for frontend_key, db_key in setting_map.items():
            if frontend_key in settings:
                value = settings[frontend_key]
                if isinstance(value, bool):
                    value = "true" if value else "false"
                else:
                    value = str(value)
                
                SettingsService.set_setting(
                    db,
                    db_key,
                    value,
                    description=f"Grading setting: {frontend_key}",
                    encrypt=False,
                    user_id=current_user.id
                )
                saved_count += 1
        
        return {
            "message": f"Successfully saved {saved_count} grading settings",
            "saved_count": saved_count,
            "updated_by": current_user.email
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save grading settings: {str(e)}"
        )


@router.get("/workflow", response_model=Dict[str, Any])
def get_workflow_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    """
    Get workflow and approval settings (Admin only)
    """
    try:
        settings = SettingsService.get_all_settings(db, include_encrypted=False)
        
        return {
            # Approval Rules
            "requireHodApproval": settings.get("require_hod_approval", "true").lower() == "true",
            "hodCanReject": settings.get("hod_can_reject", "false").lower() == "true",
            "hodCanBypass": settings.get("hod_can_bypass", "false").lower() == "true",
            "hodReviewDays": int(settings.get("hod_review_days", "3")),
            "requireAcademicApproval": settings.get("require_academic_approval", "true").lower() == "true",
            "academicCanReject": settings.get("academic_can_reject", "true").lower() == "true",
            "academicAutoPublish": settings.get("academic_auto_publish", "true").lower() == "true",
            "academicReviewDays": int(settings.get("academic_review_days", "5")),
            
            # Routing Rules
            "autoRouteToHod": settings.get("auto_route_to_hod", "true").lower() == "true",
            "autoRouteToAcademic": settings.get("auto_route_to_academic", "true").lower() == "true",
            "routeByDepartment": settings.get("route_by_department", "true").lower() == "true",
            "parallelApproval": settings.get("parallel_approval", "false").lower() == "true",
            "escalateOverdue": settings.get("escalate_overdue", "false").lower() == "true",
            "escalationLevel": settings.get("escalation_level", "academic_head"),
            
            # Deadlines
            "submissionDeadlineDays": int(settings.get("submission_deadline_days", "30")),
            "draftSavePeriod": int(settings.get("draft_save_period", "90")),
            "revisionDeadline": int(settings.get("revision_deadline", "7")),
            "reminderBeforeDays": int(settings.get("reminder_before_days", "2")),
            "maxPendingDays": int(settings.get("max_pending_days", "14")),
            "strictDeadlines": settings.get("strict_deadlines", "false").lower() == "true",
            
            # Notifications
            "notifyOnSubmit": settings.get("notify_on_submit", "true").lower() == "true",
            "notifyOnApproval": settings.get("notify_on_approval", "true").lower() == "true",
            "notifyOnRejection": settings.get("notify_on_rejection", "true").lower() == "true",
            "notifyOnDeadline": settings.get("notify_on_deadline", "true").lower() == "true",
            "inAppNewTask": settings.get("in_app_new_task", "true").lower() == "true",
            "inAppStatusChange": settings.get("in_app_status_change", "true").lower() == "true",
            "inAppComments": settings.get("in_app_comments", "true").lower() == "true",
            "notificationFrequency": settings.get("notification_frequency", "instant")
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load workflow settings: {str(e)}"
        )


@router.post("/workflow")
def save_workflow_settings(
    settings: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    """
    Save workflow and approval settings (Admin only)
    """
    try:
        setting_map = {
            "requireHodApproval": "require_hod_approval",
            "hodCanReject": "hod_can_reject",
            "hodCanBypass": "hod_can_bypass",
            "hodReviewDays": "hod_review_days",
            "requireAcademicApproval": "require_academic_approval",
            "academicCanReject": "academic_can_reject",
            "academicAutoPublish": "academic_auto_publish",
            "academicReviewDays": "academic_review_days",
            "autoRouteToHod": "auto_route_to_hod",
            "autoRouteToAcademic": "auto_route_to_academic",
            "routeByDepartment": "route_by_department",
            "parallelApproval": "parallel_approval",
            "escalateOverdue": "escalate_overdue",
            "escalationLevel": "escalation_level",
            "submissionDeadlineDays": "submission_deadline_days",
            "draftSavePeriod": "draft_save_period",
            "revisionDeadline": "revision_deadline",
            "reminderBeforeDays": "reminder_before_days",
            "maxPendingDays": "max_pending_days",
            "strictDeadlines": "strict_deadlines",
            "notifyOnSubmit": "notify_on_submit",
            "notifyOnApproval": "notify_on_approval",
            "notifyOnRejection": "notify_on_rejection",
            "notifyOnDeadline": "notify_on_deadline",
            "inAppNewTask": "in_app_new_task",
            "inAppStatusChange": "in_app_status_change",
            "inAppComments": "in_app_comments",
            "notificationFrequency": "notification_frequency"
        }
        
        saved_count = 0
        for frontend_key, db_key in setting_map.items():
            if frontend_key in settings:
                value = settings[frontend_key]
                if isinstance(value, bool):
                    value = "true" if value else "false"
                else:
                    value = str(value)
                
                SettingsService.set_setting(
                    db,
                    db_key,
                    value,
                    description=f"Workflow setting: {frontend_key}",
                    encrypt=False,
                    user_id=current_user.id
                )
                saved_count += 1
        
        return {
            "message": f"Successfully saved {saved_count} workflow settings",
            "saved_count": saved_count,
            "updated_by": current_user.email
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save workflow settings: {str(e)}"
        )


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
