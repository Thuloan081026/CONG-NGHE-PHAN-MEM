from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...core.database import get_db
from ...core.deps import get_current_user
from ...models.user import User
from ...schemas.clo_schema import (
    CLOCreate, CLOUpdate, CLOResponse,
    PLOCreate, PLOUpdate, PLOResponse,
    MappingCreate, MappingUpdate, MappingResponse
)
from ...services.clo_service import CLOService

router = APIRouter(prefix="/clo-plo", tags=["clo-plo"])


# CLO endpoints
@router.post("/clo", response_model=CLOResponse, status_code=status.HTTP_201_CREATED)
def create_clo(
    clo_data: CLOCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new CLO"""
    return CLOService.create_clo(db=db, clo_data=clo_data, current_user=current_user)


@router.get("/clo/syllabus/{syllabus_id}", response_model=List[CLOResponse])
def get_clos(
    syllabus_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all CLOs for a syllabus"""
    return CLOService.get_clos_by_syllabus(db, syllabus_id)


@router.patch("/clo/{clo_id}", response_model=CLOResponse)
def update_clo(
    clo_id: int,
    clo_data: CLOUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a CLO"""
    return CLOService.update_clo(db=db, clo_id=clo_id, update_data=clo_data, current_user=current_user)


@router.delete("/clo/{clo_id}")
def delete_clo(
    clo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a CLO"""
    CLOService.delete_clo(db, clo_id, current_user)
    return {"message": "CLO deleted successfully"}


# PLO endpoints
@router.post("/plo", response_model=PLOResponse, status_code=status.HTTP_201_CREATED)
def create_plo(
    plo_data: PLOCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new PLO"""
    from ...services.clo_service import PLOService
    return PLOService.create_plo(db=db, plo_data=plo_data, current_user=current_user)


@router.get("/plo", response_model=List[PLOResponse])
def get_plos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all PLOs"""
    from ...services.clo_service import PLOService
    return PLOService.get_all_plos(db)


@router.patch("/plo/{plo_id}", response_model=PLOResponse)
def update_plo(
    plo_id: int,
    plo_data: PLOUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a PLO"""
    from ...services.clo_service import PLOService
    return PLOService.update_plo(db=db, plo_id=plo_id, update_data=plo_data, current_user=current_user)


@router.delete("/plo/{plo_id}")
def delete_plo(
    plo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a PLO"""
    from ...services.clo_service import PLOService
    PLOService.delete_plo(db, plo_id, current_user)
    return {"message": "PLO deleted successfully"}


# Mapping endpoints
@router.post("/mapping", response_model=MappingResponse, status_code=status.HTTP_201_CREATED)
def create_mapping(
    mapping_data: MappingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new CLO-PLO mapping"""
    from ...services.clo_service import MappingService
    return MappingService.create_mapping(db=db, mapping_data=mapping_data, current_user=current_user)


@router.get("/mapping/syllabus/{syllabus_id}", response_model=List[MappingResponse])
def get_mappings(
    syllabus_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all CLO-PLO mappings for a syllabus"""
    from ...services.clo_service import MappingService
    return MappingService.get_mappings_by_syllabus(db, syllabus_id)


@router.get("/mapping/matrix/{syllabus_id}")
def get_mapping_matrix(
    syllabus_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get CLO-PLO mapping matrix for a syllabus"""
    from ...services.clo_service import MappingService
    mappings = MappingService.get_mappings_by_syllabus(db, syllabus_id)
    from ...services.clo_service import CLOService
    clos = CLOService.get_clos_by_syllabus(db, syllabus_id)
    from ...services.clo_service import PLOService
    plos = PLOService.get_all_plos(db)
    
    # Build matrix
    matrix = {
        "syllabus_id": syllabus_id,
        "clos": [{"id": c.id, "code": c.code, "description": c.description} for c in clos],
        "plos": [{"id": p.id, "code": p.code, "description": p.description} for p in plos],
        "mappings": [
            {
                "clo_id": m.clo_id,
                "plo_id": m.plo_id,
                "correlation_level": m.correlation_level,
                "correlation_score": m.correlation_score
            } for m in mappings
        ]
    }
    return matrix


@router.patch("/mapping/{mapping_id}", response_model=MappingResponse)
def update_mapping(
    mapping_id: int,
    mapping_data: MappingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a mapping"""
    from ...services.clo_service import MappingService
    return MappingService.update_mapping(db=db, mapping_id=mapping_id, update_data=mapping_data, current_user=current_user)


@router.delete("/mapping/{mapping_id}")
def delete_mapping(
    mapping_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a mapping"""
    from ...services.clo_service import MappingService
    MappingService.delete_mapping(db, mapping_id, current_user)
    return {"message": "Mapping deleted successfully"}
