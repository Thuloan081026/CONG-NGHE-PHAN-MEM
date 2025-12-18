from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status
from ..models.review import Review
from ..repositories.review_repo import review_repo


class ReviewService:
    
    def create_review(self, db: Session, syllabus_id: int, content: str, section: str, user_id: int) -> Review:
        review = Review(
            syllabus_id=syllabus_id,
            content=content,
            section=section,
            created_by=user_id
        )
        return review_repo.create(db, review)
    
    def get_reviews_by_syllabus(self, db: Session, syllabus_id: int) -> List[Review]:
        return review_repo.get_by_syllabus(db, syllabus_id)
    
    def update_review(self, db: Session, review_id: int, content: str = None, section: str = None) -> Review:
        review = review_repo.get_by_id(db, review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        if content:
            review.content = content
        if section:
            review.section = section
        
        return review_repo.update(db, review)
    
    def resolve_review(self, db: Session, review_id: int, user_id: int) -> Review:
        review = review_repo.get_by_id(db, review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        review.is_resolved = 1
        review.resolved_by = user_id
        from datetime import datetime, UTC
        review.resolved_at = datetime.now(UTC)
        
        return review_repo.update(db, review)
    
    def delete_review(self, db: Session, review_id: int):
        review = review_repo.get_by_id(db, review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        review_repo.delete(db, review)


review_service = ReviewService()
