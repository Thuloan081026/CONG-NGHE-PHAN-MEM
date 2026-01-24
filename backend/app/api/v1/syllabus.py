from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from pathlib import Path

from ...core.database import get_db
from ...core.deps import get_current_user, require_roles
from ...models.user import User
from ...schemas.syllabus_schema import (
    SyllabusCreate, SyllabusUpdate, SyllabusOut, SyllabusListOut,
    SyllabusDetailOut, SyllabusVersionOut, SyllabusVersionListOut,
    SyllabusStatusUpdate, CLOPLOMappingUpdate
)
from ...services.syllabus_service import SyllabusService, SyllabusVersionService
from ...services.notification_service import NotificationService


router = APIRouter(prefix="/syllabus", tags=["syllabus"])
syllabus_service = SyllabusService()
version_service = SyllabusVersionService()
notification_service = NotificationService()


# ==================== SYLLABUS CRUD ENDPOINTS ====================

@router.post(
    "",
    response_model=SyllabusOut,
    status_code=201,
    summary="Create new syllabus",
    description="Tạo mới giáo trình. Yêu cầu role: lecturer, hod, admin"
)
def create_syllabus(
    syllabus_in: SyllabusCreate,
    current_user: User = Depends(require_roles("lecturer", "hod", "admin")),
    db: Session = Depends(get_db)
):
    """
    Create new syllabus with initial version tracking.
    
    **Giáo trình được tạo với trạng thái "draft" (bản nháp)**
    
    Parameters:
    - subject_code: Mã môn học (phải là duy nhất)
    - subject_name: Tên môn học
    - credits: Số tín chỉ
    - semester: Kỳ học
    - objectives: Mục tiêu học tập
    - clos: Course Learning Outcomes (CLO)
    - plos: Program Learning Outcomes (PLO)
    """
    return syllabus_service.create_syllabus(db, syllabus_in, current_user.id)


@router.get(
    "",
    response_model=SyllabusListOut,
    summary="List my syllabuses",
    description="Lấy danh sách giáo trình của tôi (người dùng hiện tại)"
)
def list_my_syllabuses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    semester: Optional[int] = None,
    department: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(require_roles("lecturer", "hod", "admin")),
    db: Session = Depends(get_db)
):
    """
    List syllabuses created by current user.
    
    Query parameters:
    - skip: Số bản ghi bỏ qua (default: 0)
    - limit: Số bản ghi trả về (default: 100, max: 1000)
    - semester: Lọc theo kỳ học (tùy chọn)
    - department: Lọc theo bộ môn (tùy chọn)
    - status: Lọc theo trạng thái (draft, submitted, under_review, approved, published)
    """
    items, total = syllabus_service.list_my_syllabuses(
        db, current_user.id, skip, limit, semester, department, status
    )
    return SyllabusListOut(
        total=total,
        count=len(items),
        page=skip // limit + 1,
        page_size=limit,
        items=items
    )


@router.get(
    "/pending",
    response_model=SyllabusListOut,
    summary="List pending syllabuses for HoD review",
    description="Lấy danh sách giáo trình đang chờ HoD review (chỉ HoD và admin)"
)
def list_pending_for_hod(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(require_roles("hod", "admin")),
    db: Session = Depends(get_db)
):
    """
    List syllabuses pending HoD review.
    Only HoD and admin can access this endpoint.
    """
    from ...models.syllabus import Syllabus
    
    # Query syllabuses with status pending_hod_review or submitted
    query = db.query(Syllabus).filter(
        Syllabus.status.in_(['pending_hod_review', 'submitted', 'pending_review'])
    )
    
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    
    return SyllabusListOut(
        total=total,
        count=len(items),
        page=skip // limit + 1,
        page_size=limit,
        items=items
    )


@router.get(
    "/published",
    response_model=SyllabusListOut,
    summary="List published syllabuses",
    description="Lấy danh sách giáo trình đã được xuất bản (công khai)"
)
def list_published(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    semester: Optional[int] = None,
    department: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List published syllabuses (accessible to all users).
    
    Giáo trình này đã được phê duyệt và công khai với tất cả người dùng.
    """
    items, total = syllabus_service.list_published_syllabuses(
        db, skip, limit, semester, department
    )
    return SyllabusListOut(
        total=total,
        count=len(items),
        page=skip // limit + 1,
        page_size=limit,
        items=items
    )


@router.get(
    "/search",
    response_model=SyllabusListOut,
    summary="Search syllabuses",
    description="Tìm kiếm giáo trình theo từ khóa"
)
def search_syllabuses(
    q: str = Query(..., min_length=1, description="Keyword to search"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Search syllabuses by code, name, or description.
    
    Tìm kiếm theo mã môn, tên môn hoặc mô tả.
    """
    items, total = syllabus_service.search_syllabuses(db, q, skip, limit)
    return SyllabusListOut(
        total=total,
        count=len(items),
        page=skip // limit + 1,
        page_size=limit,
        items=items
    )


# ==================== FILE UPLOAD ENDPOINT (MUST BE BEFORE /{syllabus_id}) ====================

@router.post("/{syllabus_id}/upload-files")
async def upload_syllabus_files(
    syllabus_id: int,
    current_user: User = Depends(require_roles("lecturer", "hod", "admin")),
    db: Session = Depends(get_db),
    textbook_files: List[UploadFile] = File(default=None),
    reference_files: List[UploadFile] = File(default=None),
    learning_material_files: List[UploadFile] = File(default=None),
    course_files: List[UploadFile] = File(default=None)
):
    """Upload files for syllabus"""
    print(f"[DEBUG] Upload endpoint called for syllabus_id: {syllabus_id}")
    print(f"[DEBUG] textbook_files: {textbook_files}")
    print(f"[DEBUG] reference_files: {reference_files}")
    print(f"[DEBUG] learning_material_files: {learning_material_files}")
    print(f"[DEBUG] course_files: {course_files}")
    
    from ...models.syllabus import Syllabus
    syllabus = db.query(Syllabus).filter(Syllabus.id == syllabus_id).first()
    if not syllabus:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    
    if syllabus.created_by != current_user.id and current_user.role not in ["hod", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    base_dir = Path("data/syllabuses") / str(syllabus_id)
    base_dir.mkdir(parents=True, exist_ok=True)
    
    uploaded_files = {"textbooks": [], "references": [], "materials": [], "course_files": []}
    
    if textbook_files:
        textbook_dir = base_dir / "textbooks"
        textbook_dir.mkdir(exist_ok=True)
        for file in textbook_files:
            if file.filename:
                file_path = textbook_dir / file.filename
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                uploaded_files["textbooks"].append(str(file_path))
    
    if reference_files:
        ref_dir = base_dir / "references"
        ref_dir.mkdir(exist_ok=True)
        for file in reference_files:
            if file.filename:
                file_path = ref_dir / file.filename
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                uploaded_files["references"].append(str(file_path))
    
    if learning_material_files:
        material_dir = base_dir / "materials"
        material_dir.mkdir(exist_ok=True)
        for file in learning_material_files:
            if file.filename:
                file_path = material_dir / file.filename
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                uploaded_files["materials"].append(str(file_path))
    
    if course_files:
        course_dir = base_dir / "course_files"
        course_dir.mkdir(exist_ok=True)
        for file in course_files:
            if file.filename:
                file_path = course_dir / file.filename
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                uploaded_files["course_files"].append(str(file_path))
    
    if not syllabus.file_metadata:
        syllabus.file_metadata = {}
    syllabus.file_metadata["uploaded_files"] = uploaded_files
    print(f"[DEBUG] Saving to DB - uploaded_files: {uploaded_files}")
    db.commit()
    print(f"[DEBUG] Committed to database")
    
    return {"message": "Files uploaded successfully", "syllabus_id": syllabus_id, "uploaded_files": uploaded_files}


@router.get(
    "/{syllabus_id}",
    response_model=SyllabusDetailOut,
    summary="Get syllabus detail",
    description="Lấy chi tiết giáo trình (bao gồm lịch sử phiên bản)"
)
def get_syllabus(
    syllabus_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get syllabus details with version history.
    
    Chi tiết gồm:
    - Thông tin cơ bản (tên, mã, tín chỉ, ...)
    - Mục tiêu học tập (objectives)
    - CLO, PLO mappings
    - Các phiên bản (versions)
    """
    syllabus = syllabus_service.get_syllabus(db, syllabus_id)
    if not syllabus:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    return syllabus


@router.put(
    "/{syllabus_id}",
    response_model=SyllabusOut,
    summary="Update syllabus",
    description="Cập nhật giáo trình (tự động tạo version mới)"
)
def update_syllabus(
    syllabus_id: int,
    update_data: SyllabusUpdate,
    current_user: User = Depends(require_roles("lecturer", "hod", "admin")),
    db: Session = Depends(get_db)
):
    """
    Update syllabus and automatically create new version record.
    
    **Tính năng chính:**
    1. Cập nhật thông tin giáo trình
    2. Tự động phát hiện các trường bị thay đổi
    3. Tạo version mới với lịch sử thay đổi (changelog)
    4. Lưu giữ giá trị cũ để có thể rollback sau này
    
    **Quyền hạn:**
    - Lecturer chỉ có thể cập nhật giáo trình của mình
    - HOD và Admin có thể cập nhật bất kỳ giáo trình nào
    """
    syllabus = syllabus_service.get_syllabus(db, syllabus_id)
    if not syllabus:
        raise HTTPException(status_code=404, detail="Syllabus not found")

    # Check permission: lecturer can only update their own syllabuses
    if current_user.role == "lecturer" and syllabus.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own syllabuses")

    return syllabus_service.update_syllabus(db, syllabus_id, update_data, current_user.id)


@router.delete(
    "/{syllabus_id}",
    status_code=204,
    summary="Delete syllabus",
    description="Xóa giáo trình (bao gồm tất cả phiên bản)"
)
def delete_syllabus(
    syllabus_id: int,
    current_user: User = Depends(require_roles("hod", "admin")),
    db: Session = Depends(get_db)
):
    """
    Delete syllabus and all related versions.
    
    **Chỉ HOD và Admin có thể xóa giáo trình**
    
    Xóa này sẽ xóa:
    - Giáo trình chính
    - Tất cả các phiên bản của giáo trình
    - Tất cả metadata liên quan
    """
    success = syllabus_service.delete_syllabus(db, syllabus_id)
    if not success:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    return None


# ==================== STATUS & WORKFLOW ENDPOINTS ====================

@router.patch(
    "/{syllabus_id}/status",
    response_model=SyllabusOut,
    summary="Update syllabus status",
    description="Cập nhật trạng thái quy trình giáo trình"
)
def update_status(
    syllabus_id: int,
    status_update: SyllabusStatusUpdate,
    current_user: User = Depends(require_roles("lecturer", "hod", "admin", "academic_affairs")),
    db: Session = Depends(get_db)
):
    """
    Update syllabus workflow status.
    
    **Trạng thái (Status):**
    - draft: Bản nháp (mới tạo)
    - submitted: Đã nộp để phê duyệt
    - under_review: Đang được phê duyệt
    - approved: Đã được phê duyệt
    - published: Đã xuất bản (công khai)
    
    **Quyền hạn:**
    - Lecturer có thể submit giáo trình của mình
    - HOD/Admin có thể approve/publish
    """
    syllabus = syllabus_service.update_syllabus_status(
        db, syllabus_id, status_update.status
    )

    if not syllabus:
        raise HTTPException(status_code=404, detail="Syllabus not found")

    subject = syllabus.subject_name

    # ===== FE-05: AUTO NOTIFICATION =====
    if status_update.status == "submitted":
        # Thông báo cho HOD
        notification_service.notify_role(
            db,
            role="hod",
            message=f"Syllabus '{subject}' đã được gửi để duyệt"
        )

    elif status_update.status == "under_review":
        # Thông báo cho người tạo
        notification_service.create_notification(
            db=db,
            user_id=syllabus.created_by,
            message=f"Syllabus '{subject}' đang được Phòng Đào tạo xem xét"
        )

    elif status_update.status == "approved":
        notification_service.create_notification(
            db=db,
            user_id=syllabus.created_by,
            message=f"Syllabus '{subject}' đã được phê duyệt"
        )

    elif status_update.status == "rejected":
        notification_service.create_notification(
            db=db,
            user_id=syllabus.created_by,
            message=f"Syllabus '{subject}' bị từ chối và cần chỉnh sửa"
        )

    return syllabus


@router.post(
    "/{syllabus_id}/publish",
    response_model=SyllabusOut,
    summary="Publish syllabus",
    description="Xuất bản giáo trình (chỉ khi đã approved)"
)
def publish_syllabus(
    syllabus_id: int,
    current_user: User = Depends(require_roles("hod", "admin")),
    db: Session = Depends(get_db)
):
    """
    Publish syllabus to make it public.
    
    **Điều kiện:**
    - Giáo trình phải có trạng thái "approved"
    - Chỉ HOD/Admin có thể publish
    """
    syllabus = syllabus_service.publish_syllabus(db, syllabus_id)

    if not syllabus:
        raise HTTPException(status_code=404, detail="Syllabus not found")

    # Thông báo cho người tạo khi được publish
    notification_service.create_notification(
        db=db,
        user_id=syllabus.created_by,
        message=f"Syllabus '{syllabus.subject_name}' đã được xuất bản"
    )

    # Thông báo cho tất cả người follow
    notification_service.notify_followers(
        db,
        syllabus.id,
        f"Syllabus '{syllabus.subject_name}' vừa được xuất bản"
    )

    return syllabus



# ==================== CLO/PLO MAPPING ENDPOINTS ====================

@router.patch(
    "/{syllabus_id}/clo-plo-mapping",
    response_model=SyllabusOut,
    summary="Update CLO-PLO mapping",
    description="Cập nhật mapping giữa CLO và PLO"
)
def update_clo_plo_mapping(
    syllabus_id: int,
    mapping_data: CLOPLOMappingUpdate,
    current_user: User = Depends(require_roles("lecturer", "hod", "admin")),
    db: Session = Depends(get_db)
):
    """
    Update CLO (Course Learning Outcomes) to PLO (Program Learning Outcomes) mapping.
    
    **CLO-PLO Mapping:**
    Ánh xạ giữa mục tiêu môn học (CLO) và mục tiêu chương trình (PLO).
    
    Ví dụ:
    ```json
    {
        "CLO1": ["PLO1", "PLO3"],
        "CLO2": ["PLO2", "PLO3"],
        "CLO3": ["PLO1"]
    }
    ```
    """
    update_data = SyllabusUpdate(clo_plo_mapping=mapping_data.clo_plo_mapping)
    return syllabus_service.update_syllabus(db, syllabus_id, update_data, current_user.id)


# ==================== VERSION CONTROL ENDPOINTS ====================

@router.get(
    "/{syllabus_id}/versions",
    response_model=SyllabusVersionListOut,
    summary="List syllabus versions",
    description="Lấy danh sách tất cả phiên bản của giáo trình"
)
def list_versions(
    syllabus_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all versions of a syllabus with pagination.
    
    **Lịch sử phiên bản:**
    Mỗi lần cập nhật giáo trình, hệ thống tự động tạo phiên bản mới để lưu giữ.
    
    Mỗi phiên bản ghi lại:
    - Số phiên bản
    - Các trường bị thay đổi
    - Giá trị cũ và giá trị mới
    - Thời gian thay đổi
    - Người tạo thay đổi
    """
    # Check if syllabus exists
    syllabus = syllabus_service.get_syllabus(db, syllabus_id)
    if not syllabus:
        raise HTTPException(status_code=404, detail="Syllabus not found")

    versions, total = version_service.list_versions(db, syllabus_id, skip, limit)
    return SyllabusVersionListOut(total=total, versions=versions)


@router.get(
    "/{syllabus_id}/versions/latest",
    response_model=SyllabusVersionOut,
    summary="Get latest version",
    description="Lấy phiên bản mới nhất của giáo trình"
)
def get_latest_version(
    syllabus_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the latest version of a syllabus.
    
    Trả về phiên bản được tạo gần đây nhất.
    """
    version = version_service.get_latest_version(db, syllabus_id)
    if not version:
        raise HTTPException(status_code=404, detail="No versions found for this syllabus")
    return version


@router.get(
    "/{syllabus_id}/versions/{version_id}",
    response_model=SyllabusVersionOut,
    summary="Get specific version",
    description="Lấy một phiên bản cụ thể của giáo trình"
)
def get_version(
    syllabus_id: int,
    version_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific version of a syllabus.
    
    Xem chi tiết một phiên bản cụ thể (bao gồm changelog).
    """
    version = version_service.get_version(db, version_id)
    if not version or version.syllabus_id != syllabus_id:
        raise HTTPException(status_code=404, detail="Version not found")
    return version


@router.post(
    "/{syllabus_id}/versions/{version_id}/rollback",
    response_model=SyllabusOut,
    summary="Rollback to version",
    description="Khôi phục giáo trình về một phiên bản cũ"
)
def rollback_version(
    syllabus_id: int,
    version_id: int,
    current_user: User = Depends(require_roles("lecturer", "hod", "admin")),
    db: Session = Depends(get_db)
):
    """
    Rollback syllabus to a specific previous version.
    
    **Tính năng Rollback:**
    - Khôi phục toàn bộ nội dung từ phiên bản cũ
    - Tự động tạo phiên bản mới để ghi lại thao tác rollback
    - Có thể dùng để hoàn tác những thay đổi không mong muốn
    
    Ví dụ: Nếu phiên bản hiện tại là v5, bạn có thể rollback về v3
    """
    return version_service.rollback_to_version(db, syllabus_id, version_id, current_user.id)


@router.get(
    "/{syllabus_id}/versions/{version_id_1}/compare/{version_id_2}",
    summary="Compare two versions",
    description="So sánh hai phiên bản khác nhau"
)
def compare_versions(
    syllabus_id: int,
    version_id_1: int,
    version_id_2: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Compare two versions and show what changed.
    
    **So sánh phiên bản:**
    Hiển thị tất cả các khác biệt giữa hai phiên bản (diff).
    
    Bao gồm:
    - Danh sách các trường thay đổi
    - Giá trị cũ của mỗi trường
    - Giá trị mới của mỗi trường
    """
    comparison = version_service.compare_versions(db, version_id_1, version_id_2)
    if not comparison:
        raise HTTPException(status_code=404, detail="One or both versions not found")
    return comparison
