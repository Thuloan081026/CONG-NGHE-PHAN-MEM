from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.clo import CLO
from ..models.plo import PLO
from ..models.clo_plo import CLO_PLO_Mapping


class CLORepository:
    """Repository for CLO operations"""
    
    def create_clo(self, db: Session, syllabus_id: int, code: str, description: str, 
                   cognitive_level: str = None, weight: float = 1.0) -> CLO:
        """Create a new CLO"""
        clo = CLO(
            syllabus_id=syllabus_id,
            code=code,
            description=description,
            cognitive_level=cognitive_level,
            weight=weight
        )
        db.add(clo)
        db.commit()
        db.refresh(clo)
        return clo
    
    def get_clo_by_id(self, db: Session, clo_id: int) -> Optional[CLO]:
        """Get CLO by ID"""
        return db.query(CLO).filter(CLO.id == clo_id).first()
    
    def get_clos_by_syllabus(self, db: Session, syllabus_id: int) -> List[CLO]:
        """Get all CLOs for a syllabus"""
        return db.query(CLO).filter(CLO.syllabus_id == syllabus_id).all()
    
    def update_clo(self, db: Session, clo_id: int, **kwargs) -> CLO:
        """Update a CLO"""
        clo = self.get_clo_by_id(db, clo_id)
        if clo:
            for key, value in kwargs.items():
                if hasattr(clo, key) and value is not None:
                    setattr(clo, key, value)
            db.commit()
            db.refresh(clo)
        return clo
    
    def delete_clo(self, db: Session, clo_id: int) -> bool:
        """Delete a CLO"""
        clo = self.get_clo_by_id(db, clo_id)
        if clo:
            db.delete(clo)
            db.commit()
            return True
        return False


class PLORepository:
    """Repository for PLO operations"""
    
    def create_plo(self, db: Session, code: str, description: str, program_code: str = None,
                   program_name: str = None, category: str = None, weight: float = 1.0) -> PLO:
        """Create a new PLO"""
        plo = PLO(
            code=code,
            description=description,
            program_code=program_code,
            program_name=program_name,
            category=category,
            weight=weight
        )
        db.add(plo)
        db.commit()
        db.refresh(plo)
        return plo
    
    def get_plo_by_id(self, db: Session, plo_id: int) -> Optional[PLO]:
        """Get PLO by ID"""
        return db.query(PLO).filter(PLO.id == plo_id).first()
    
    def get_plo_by_code(self, db: Session, code: str) -> Optional[PLO]:
        """Get PLO by code"""
        return db.query(PLO).filter(PLO.code == code).first()
    
    def get_all_plos(self, db: Session, program_code: str = None) -> List[PLO]:
        """Get all PLOs, optionally filtered by program"""
        query = db.query(PLO)
        if program_code:
            query = query.filter(PLO.program_code == program_code)
        return query.all()
    
    def update_plo(self, db: Session, plo_id: int, **kwargs) -> PLO:
        """Update a PLO"""
        plo = self.get_plo_by_id(db, plo_id)
        if plo:
            for key, value in kwargs.items():
                if hasattr(plo, key) and value is not None:
                    setattr(plo, key, value)
            db.commit()
            db.refresh(plo)
        return plo
    
    def delete_plo(self, db: Session, plo_id: int) -> bool:
        """Delete a PLO"""
        plo = self.get_plo_by_id(db, plo_id)
        if plo:
            db.delete(plo)
            db.commit()
            return True
        return False


class MappingRepository:
    """Repository for CLO-PLO Mapping operations"""
    
    def create_mapping(self, db: Session, clo_id: int, plo_id: int, 
                      correlation_level: str = None, correlation_score: float = None,
                      ai_suggested: int = 0, ai_confidence: float = None,
                      notes: str = None) -> CLO_PLO_Mapping:
        """Create a new mapping"""
        mapping = CLO_PLO_Mapping(
            clo_id=clo_id,
            plo_id=plo_id,
            correlation_level=correlation_level,
            correlation_score=correlation_score,
            ai_suggested=ai_suggested,
            ai_confidence=ai_confidence,
            notes=notes
        )
        db.add(mapping)
        db.commit()
        db.refresh(mapping)
        return mapping
    
    def get_mapping_by_id(self, db: Session, mapping_id: int) -> Optional[CLO_PLO_Mapping]:
        """Get mapping by ID"""
        return db.query(CLO_PLO_Mapping).filter(CLO_PLO_Mapping.id == mapping_id).first()
    
    def get_mapping_by_clo_plo(self, db: Session, clo_id: int, plo_id: int) -> Optional[CLO_PLO_Mapping]:
        """Get mapping by CLO and PLO IDs"""
        return db.query(CLO_PLO_Mapping).filter(
            CLO_PLO_Mapping.clo_id == clo_id,
            CLO_PLO_Mapping.plo_id == plo_id
        ).first()
    
    def get_mappings_by_syllabus(self, db: Session, syllabus_id: int) -> List[CLO_PLO_Mapping]:
        """Get all mappings for a syllabus"""
        return db.query(CLO_PLO_Mapping).join(CLO).filter(CLO.syllabus_id == syllabus_id).all()
    
    def get_mappings_by_clo(self, db: Session, clo_id: int) -> List[CLO_PLO_Mapping]:
        """Get all mappings for a CLO"""
        return db.query(CLO_PLO_Mapping).filter(CLO_PLO_Mapping.clo_id == clo_id).all()
    
    def get_mappings_by_plo(self, db: Session, plo_id: int) -> List[CLO_PLO_Mapping]:
        """Get all mappings for a PLO"""
        return db.query(CLO_PLO_Mapping).filter(CLO_PLO_Mapping.plo_id == plo_id).all()
    
    def update_mapping(self, db: Session, mapping_id: int, **kwargs) -> CLO_PLO_Mapping:
        """Update a mapping"""
        mapping = self.get_mapping_by_id(db, mapping_id)
        if mapping:
            for key, value in kwargs.items():
                if hasattr(mapping, key) and value is not None:
                    setattr(mapping, key, value)
            db.commit()
            db.refresh(mapping)
        return mapping
    
    def delete_mapping(self, db: Session, mapping_id: int) -> bool:
        """Delete a mapping"""
        mapping = self.get_mapping_by_id(db, mapping_id)
        if mapping:
            db.delete(mapping)
            db.commit()
            return True
        return False


# Create singleton instances
clo_repo = CLORepository()
plo_repo = PLORepository()
mapping_repo = MappingRepository()
