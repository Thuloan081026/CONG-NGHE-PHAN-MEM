from fastapi import APIRouter
from services.ai_service import AIService
from schemas.ai_schema import (
    SummaryRequest, SummaryResponse,
    DiffRequest, DiffResponse,
    CLOCheckRequest, CLOCheckResponse
)

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/summary", response_model=SummaryResponse)
def summarize(req: SummaryRequest):
    task_id = AIService.create_summary(req.content, req.syllabus_id)
    return SummaryResponse(task_id=task_id)

@router.post("/diff", response_model=DiffResponse)
def diff(req: DiffRequest):
    task_id = AIService.create_diff(req.old_content, req.new_content, req.syllabus_id)
    return DiffResponse(task_id=task_id)

@router.post("/clo-check", response_model=CLOCheckResponse)
def check_clo(req: CLOCheckRequest):
    task_id = AIService.check_clo(req.clos, req.plos, req.syllabus_id)
    return CLOCheckResponse(task_id=task_id)
