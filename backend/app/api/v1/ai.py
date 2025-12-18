"""
AI Integration API - Summary, Diff, CLO Check
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...core.database import get_db
from ...core.deps import get_current_user
from ...models.user import User
from ...services.ai_service import AIService
from ...schemas.ai_schema import (
    SummarizeRequest, SummarizeResponse,
    DiffRequest, DiffResponse,
    CLOCheckRequest, CLOCheckResponse
)

router = APIRouter(prefix="/ai", tags=["AI Integration"])
ai_service = AIService()


@router.post("/summarize", response_model=SummarizeResponse)
def summarize_syllabus(
    request: SummarizeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    AI auto-summarize syllabus content
    
    **Tự động tóm tắt nội dung giáo trình**
    - Trích xuất các điểm chính
    - Tạo tóm tắt ngắn gọn
    - Hỗ trợ tiếng Việt/English
    """
    return ai_service.summarize(
        db, 
        request.syllabus_id, 
        request.language
    )


@router.post("/diff", response_model=DiffResponse)
def semantic_diff(
    request: DiffRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    AI semantic diff between two versions
    
    **So sánh ngữ nghĩa giữa 2 phiên bản**
    - Phát hiện thay đổi lớn/nhỏ
    - Phân tích mức độ ảnh hưởng
    - Tính similarity score
    """
    return ai_service.semantic_diff(
        db,
        request.version_id_1,
        request.version_id_2,
        request.language
    )


@router.post("/clo-check", response_model=CLOCheckResponse)
def check_clo_similarity(
    request: CLOCheckRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Check for similar CLOs across syllabuses
    
    **Gợi ý CLO tương tự từ các giáo trình khác**
    - Tìm kiếm CLO có nội dung tương tự
    - Tính similarity score
    - Giúp tái sử dụng CLO đã có
    """
    return ai_service.check_clo_similarity(
        db,
        request.syllabus_id,
        request.clo_description
    )


@router.get("/health")
def ai_health_check():
    """Check AI service status"""
    return {
        "status": "healthy",
        "service": "AI Integration",
        "model": "gemini-pro",
        "gemini_available": False,  # Will be True when API key is configured
        "fallback_available": True,
        "features": ["summarize", "diff", "clo-check"]
    }
