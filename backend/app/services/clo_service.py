from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status

from ..repositories.clo_repo import clo_repo, plo_repo, mapping_repo
from ..repositories.syllabus_repo import SyllabusRepository
from ..schemas.clo_schema import (
    CLOCreate, CLOUpdate, CLOResponse,
    PLOCreate, PLOUpdate, PLOResponse,
    MappingCreate, MappingUpdate, MappingResponse,
    SyllabusMappingMatrix, BulkCLOCreate, BulkMappingCreate
)
from ..models.clo import CLO
from ..models.plo import PLO
from ..models.clo_plo import CLO_PLO_Mapping
from ..models.user import User

# Initialize syllabus repository
syllabus_repo = SyllabusRepository()


class CLOService:
    """Service layer for CLO operations"""

    @staticmethod
    def create_clo(db: Session, clo_data: CLOCreate, current_user: User) -> CLOResponse:
        """Create a new CLO"""
        # Verify syllabus exists
        syllabus = syllabus_repo.get_by_id(db, clo_data.syllabus_id)
        if not syllabus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Syllabus with id {clo_data.syllabus_id} not found"
            )
        
        # Check authorization: only syllabus creator or admin/hod
        if syllabus.created_by != current_user.id and current_user.role not in ["admin", "hod", "academic_affairs"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to add CLOs to this syllabus"
            )
        
        # Create CLO
        clo = clo_repo.create_clo(
            db=db,
            syllabus_id=clo_data.syllabus_id,
            code=clo_data.code,
            description=clo_data.description,
            cognitive_level=clo_data.cognitive_level,
            weight=clo_data.weight
        )
        
        return CLOResponse.model_validate(clo)

    @staticmethod
    def get_clos_by_syllabus(db: Session, syllabus_id: int) -> List[CLOResponse]:
        """Get all CLOs for a syllabus"""
        # Verify syllabus exists
        syllabus = syllabus_repo.get_by_id(db, syllabus_id)
        if not syllabus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Syllabus with id {syllabus_id} not found"
            )
        
        clos = clo_repo.get_clos_by_syllabus(db, syllabus_id)
        return [CLOResponse.model_validate(clo) for clo in clos]

    @staticmethod
    def update_clo(db: Session, clo_id: int, update_data: CLOUpdate, current_user: User) -> CLOResponse:
        """Update a CLO"""
        clo = clo_repo.get_clo_by_id(db, clo_id)
        if not clo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"CLO with id {clo_id} not found"
            )
        
        # Check authorization
        syllabus = syllabus_repo.get_by_id(db, clo.syllabus_id)
        if syllabus.created_by != current_user.id and current_user.role not in ["admin", "hod", "academic_affairs"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this CLO"
            )
        
        # Update
        update_dict = update_data.model_dump(exclude_unset=True)
        updated_clo = clo_repo.update_clo(db, clo_id, **update_dict)
        
        return CLOResponse.model_validate(updated_clo)

    @staticmethod
    def delete_clo(db: Session, clo_id: int, current_user: User) -> dict:
        """Delete a CLO"""
        clo = clo_repo.get_clo_by_id(db, clo_id)
        if not clo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"CLO with id {clo_id} not found"
            )
        
        # Check authorization
        syllabus = syllabus_repo.get_by_id(db, clo.syllabus_id)
        if syllabus.created_by != current_user.id and current_user.role not in ["admin", "hod", "academic_affairs"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this CLO"
            )
        
        success = clo_repo.delete_clo(db, clo_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete CLO"
            )
        
        return {"message": "CLO deleted successfully", "deleted_id": clo_id}


class PLOService:
    """Service layer for PLO operations"""

    @staticmethod
    def create_plo(db: Session, plo_data: PLOCreate, current_user: User) -> PLOResponse:
        """Create a new PLO"""
        # Only admin, hod, or academic_affairs can create PLOs
        if current_user.role not in ["admin", "hod", "academic_affairs"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can create PLOs"
            )
        
        # Check if PLO code already exists
        existing = plo_repo.get_plo_by_code(db, plo_data.code)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"PLO with code {plo_data.code} already exists"
            )
        
        plo = plo_repo.create_plo(
            db=db,
            code=plo_data.code,
            description=plo_data.description,
            program_code=plo_data.program_code,
            program_name=plo_data.program_name,
            category=plo_data.category,
            weight=plo_data.weight
        )
        
        return PLOResponse.model_validate(plo)

    @staticmethod
    def get_all_plos(db: Session, program_code: Optional[str] = None) -> List[PLOResponse]:
        """Get all PLOs, optionally filtered by program"""
        plos = plo_repo.get_all_plos(db, program_code)
        return [PLOResponse.model_validate(plo) for plo in plos]

    @staticmethod
    def update_plo(db: Session, plo_id: int, update_data: PLOUpdate, current_user: User) -> PLOResponse:
        """Update a PLO"""
        if current_user.role not in ["admin", "hod", "academic_affairs"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can update PLOs"
            )
        
        plo = plo_repo.get_plo_by_id(db, plo_id)
        if not plo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"PLO with id {plo_id} not found"
            )
        
        update_dict = update_data.model_dump(exclude_unset=True)
        updated_plo = plo_repo.update_plo(db, plo_id, **update_dict)
        
        return PLOResponse.model_validate(updated_plo)

    @staticmethod
    def delete_plo(db: Session, plo_id: int, current_user: User) -> dict:
        """Delete a PLO"""
        if current_user.role not in ["admin", "hod", "academic_affairs"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can delete PLOs"
            )
        
        plo = plo_repo.get_plo_by_id(db, plo_id)
        if not plo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"PLO with id {plo_id} not found"
            )
        
        success = plo_repo.delete_plo(db, plo_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete PLO"
            )
        
        return {"message": "PLO deleted successfully", "deleted_id": plo_id}


class MappingService:
    """Service layer for CLO-PLO Mapping operations"""

    @staticmethod
    def create_mapping(db: Session, mapping_data: MappingCreate, current_user: User) -> MappingResponse:
        """Create a new CLO-PLO mapping"""
        # Verify CLO exists
        clo = clo_repo.get_clo_by_id(db, mapping_data.clo_id)
        if not clo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"CLO with id {mapping_data.clo_id} not found"
            )
        
        # Verify PLO exists
        plo = plo_repo.get_plo_by_id(db, mapping_data.plo_id)
        if not plo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"PLO with id {mapping_data.plo_id} not found"
            )
        
        # Check if mapping already exists
        existing = mapping_repo.get_mapping_by_clo_plo(db, mapping_data.clo_id, mapping_data.plo_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mapping between CLO {mapping_data.clo_id} and PLO {mapping_data.plo_id} already exists"
            )
        
        # Check authorization
        syllabus = syllabus_repo.get_by_id(db, clo.syllabus_id)
        if syllabus.created_by != current_user.id and current_user.role not in ["admin", "hod", "academic_affairs"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to create mappings for this syllabus"
            )
        
        # Create mapping
        mapping = mapping_repo.create_mapping(
            db=db,
            clo_id=mapping_data.clo_id,
            plo_id=mapping_data.plo_id,
            correlation_level=mapping_data.correlation_level,
            correlation_score=mapping_data.correlation_score,
            ai_suggested=mapping_data.ai_suggested or 0,
            ai_confidence=mapping_data.ai_confidence,
            notes=mapping_data.notes
        )
        
        # Reload with relationships
        mapping = mapping_repo.get_mapping_by_id(db, mapping.id)
        return MappingService._format_mapping_response(mapping)

    @staticmethod
    def get_mappings_by_syllabus(db: Session, syllabus_id: int) -> List[MappingResponse]:
        """Get all mappings for a syllabus"""
        # Verify syllabus exists
        syllabus = syllabus_repo.get_by_id(db, syllabus_id)
        if not syllabus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Syllabus with id {syllabus_id} not found"
            )
        
        mappings = mapping_repo.get_mappings_by_syllabus(db, syllabus_id)
        return [MappingService._format_mapping_response(m) for m in mappings]

    @staticmethod
    def get_mapping_matrix(db: Session, syllabus_id: int) -> SyllabusMappingMatrix:
        """Get complete mapping matrix for a syllabus"""
        # Verify syllabus exists
        syllabus = syllabus_repo.get_by_id(db, syllabus_id)
        if not syllabus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Syllabus with id {syllabus_id} not found"
            )
        
        clos = clo_repo.get_clos_by_syllabus(db, syllabus_id)
        mappings = mapping_repo.get_mappings_by_syllabus(db, syllabus_id)
        
        # Get unique PLOs from mappings
        plo_ids = set(m.plo_id for m in mappings)
        plos = [plo_repo.get_plo_by_id(db, plo_id) for plo_id in plo_ids]
        plos = [p for p in plos if p is not None]
        
        return SyllabusMappingMatrix(
            syllabus_id=syllabus_id,
            clos=[CLOResponse.model_validate(c) for c in clos],
            plos=[PLOResponse.model_validate(p) for p in plos],
            mappings=[MappingService._format_mapping_response(m) for m in mappings]
        )

    @staticmethod
    def update_mapping(db: Session, mapping_id: int, update_data: MappingUpdate, 
                      current_user: User) -> MappingResponse:
        """Update a mapping"""
        mapping = mapping_repo.get_mapping_by_id(db, mapping_id)
        if not mapping:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mapping with id {mapping_id} not found"
            )
        
        # Check authorization
        clo = clo_repo.get_clo_by_id(db, mapping.clo_id)
        syllabus = syllabus_repo.get_by_id(db, clo.syllabus_id)
        if syllabus.created_by != current_user.id and current_user.role not in ["admin", "hod", "academic_affairs"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this mapping"
            )
        
        update_dict = update_data.model_dump(exclude_unset=True)
        updated_mapping = mapping_repo.update_mapping(db, mapping_id, **update_dict)
        
        # Reload with relationships
        updated_mapping = mapping_repo.get_mapping_by_id(db, mapping_id)
        return MappingService._format_mapping_response(updated_mapping)

    @staticmethod
    def delete_mapping(db: Session, mapping_id: int, current_user: User) -> dict:
        """Delete a mapping"""
        mapping = mapping_repo.get_mapping_by_id(db, mapping_id)
        if not mapping:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mapping with id {mapping_id} not found"
            )
        
        # Check authorization
        clo = clo_repo.get_clo_by_id(db, mapping.clo_id)
        syllabus = syllabus_repo.get_by_id(db, clo.syllabus_id)
        if syllabus.created_by != current_user.id and current_user.role not in ["admin", "hod", "academic_affairs"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this mapping"
            )
        
        success = mapping_repo.delete_mapping(db, mapping_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete mapping"
            )
        
        return {"message": "Mapping deleted successfully", "deleted_id": mapping_id}

    @staticmethod
    def _format_mapping_response(mapping: CLO_PLO_Mapping) -> MappingResponse:
        """Helper to format mapping response with related objects"""
        response = MappingResponse.model_validate(mapping)
        if mapping.clo:
            response.clo = CLOResponse.model_validate(mapping.clo)
        if mapping.plo:
            response.plo = PLOResponse.model_validate(mapping.plo)
        return response


# Singleton instances
clo_service = CLOService()
plo_service = PLOService()
mapping_service = MappingService()
