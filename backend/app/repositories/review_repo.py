from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from ..models.review import Review


class ReviewRepository:
    
    def create(self, db: Session, review: Review) -> Review:
        db.add(review)
        db.commit()
        db.refresh(review)
        # Load author relationship
        review = db.query(Review).options(joinedload(Review.author)).filter(Review.id == review.id).first()
        return review
    
    def get_by_id(self, db: Session, review_id: int) -> Optional[Review]:
        return db.query(Review).options(joinedload(Review.author)).filter(Review.id == review_id).first()
    
    def get_by_syllabus(self, db: Session, syllabus_id: int) -> List[Review]:
        return db.query(Review).options(joinedload(Review.author)).filter(Review.syllabus_id == syllabus_id).all()
    
    def update(self, db: Session, review: Review) -> Review:
        db.commit()
        db.refresh(review)
        # Load author relationship
        review = db.query(Review).options(joinedload(Review.author)).filter(Review.id == review.id).first()
        return review
    
    def delete(self, db: Session, review: Review):
        db.delete(review)
        db.commit()


review_repo = ReviewRepository()
