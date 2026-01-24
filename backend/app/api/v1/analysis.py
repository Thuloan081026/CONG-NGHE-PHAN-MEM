from fastapi import APIRouter

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.get("/compare")
def compare_syllabus(a_id: int, b_id: int):
    # Sau này lấy từ DB, hiện mock
    return {
        "syllabus_a": a_id,
        "syllabus_b": b_id,
        "differences": {
            "credits": "3 vs 4",
            "CLO": "CLO2 missing in B"
        }
    }

@router.get("/clo-plo")
def clo_plo_chart(syllabus_id: int):
    return {
        "syllabus_id": syllabus_id,
        "mapping": [
            {"CLO": "CLO1", "PLO": "PLO2"},
            {"CLO": "CLO2", "PLO": "PLO3"}
        ]
    }
