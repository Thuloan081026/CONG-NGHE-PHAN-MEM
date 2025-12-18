from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...core.database import get_db
from ...core.deps import get_current_user
from ...models.user import User
from ...models.review import Review
from ...schemas.review_schema import ReviewCreate, ReviewUpdate, ReviewResponse
from ...services.review_service import review_service

router = APIRouter(prefix="/review", tags=["review"])


def review_to_response(review: Review) -> dict:
    """Convert Review model to response dict with author_email"""
    return {
        "id": review.id,
        "syllabus_id": review.syllabus_id,
        "content": review.content,
        "section": review.section,
        "created_by": review.created_by,
        "author_email": review.author.email if review.author else None,
        "is_resolved": review.is_resolved,
        "resolved_by": review.resolved_by,
        "resolved_at": review.resolved_at,
        "created_at": review.created_at,
        "updated_at": review.updated_at
    }


@router.post("/comment", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new review comment"""
    from sqlalchemy.exc import IntegrityError
    try:
        review = review_service.create_review(
            db=db,
            syllabus_id=review_data.syllabus_id,
            content=review_data.content,
            section=review_data.section,
            user_id=current_user.id
        )
        return review_to_response(review)
    except IntegrityError:
        raise HTTPException(status_code=404, detail="Syllabus not found")


@router.get("/syllabus/{syllabus_id}", response_model=List[ReviewResponse])
def get_reviews(
    syllabus_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all reviews for a syllabus"""
    from ...models.syllabus import Syllabus
    syllabus = db.query(Syllabus).filter(Syllabus.id == syllabus_id).first()
    if not syllabus:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    reviews = review_service.get_reviews_by_syllabus(db, syllabus_id)
    return [review_to_response(r) for r in reviews]


@router.get("/comment/{review_id}", response_model=ReviewResponse)
def get_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single review comment"""
    from ...repositories.review_repo import review_repo
    review = review_repo.get_by_id(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review_to_response(review)


@router.get("/syllabus/{syllabus_id}/unresolved", response_model=List[ReviewResponse])
def get_unresolved_reviews(
    syllabus_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get unresolved reviews for a syllabus (HOD only)"""
    if current_user.role != "hod":
        raise HTTPException(status_code=403, detail="Only HOD can view unresolved reviews")
    from ...repositories.review_repo import review_repo
    from ...models.review import Review
    reviews = db.query(Review).filter(
        Review.syllabus_id == syllabus_id,
        Review.is_resolved == 0
    ).all()
    # Load author relationship
    for r in reviews:
        db.refresh(r)
    return [review_to_response(r) for r in reviews]


@router.patch("/comment/{review_id}", response_model=ReviewResponse)
def update_review(
    review_id: int,
    review_data: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a review comment (author can edit content, HOD can resolve)"""
    from ...repositories.review_repo import review_repo
    review = review_repo.get_by_id(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check permissions
    is_author = review.created_by == current_user.id
    is_hod = current_user.role == "hod"
    
    # Only author can update content/section
    if (review_data.content or review_data.section) and not is_author:
        raise HTTPException(status_code=403, detail="Only author can update review content")
    
    # Only HOD can resolve
    if review_data.is_resolved is not None and not is_hod:
        raise HTTPException(status_code=403, detail="Only HOD can resolve reviews")
    
    # Update fields
    if review_data.is_resolved is not None and is_hod:
        updated_review = review_service.resolve_review(db, review_id, current_user.id)
    else:
        updated_review = review_service.update_review(
            db, review_id, 
            content=review_data.content,
            section=review_data.section
        )
    return review_to_response(updated_review)


@router.delete("/comment/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a review comment"""
    from ...repositories.review_repo import review_repo
    review = review_repo.get_by_id(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.created_by != current_user.id and current_user.role != "hod":
        raise HTTPException(status_code=403, detail="Only author or HOD can delete review")
    
    review_service.delete_review(db, review_id)
    return {"message": "Comment deleted successfully", "deleted_id": review_id}


@router.patch("/{review_id}/resolve", response_model=ReviewResponse)
def resolve_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Resolve a review (HOD only)"""
    from ...repositories.review_repo import review_repo
    review = review_repo.get_by_id(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if current_user.role != "hod":
        raise HTTPException(status_code=403, detail="Only HOD can resolve reviews")
    updated_review = review_service.resolve_review(db, review_id, current_user.id)
    return review_to_response(updated_review)
