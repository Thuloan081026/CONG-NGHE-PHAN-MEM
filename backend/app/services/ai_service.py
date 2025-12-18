"""
AI Service - Summary, Diff, CLO Check with Google Gemini
"""
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime
import re
from difflib import SequenceMatcher
import google.generativeai as genai

from ..models.syllabus import Syllabus, SyllabusVersion
from ..models.clo import CLO
from ..repositories.syllabus_repo import SyllabusRepository, SyllabusVersionRepository
from ..repositories.clo_repo import CLORepository
from ..schemas.ai_schema import (
    SummarizeResponse, DiffResponse, CLOCheckResponse, CLOSuggestion
)
from ..core.config import settings
from ..services.settings_service import SettingsService
from fastapi import HTTPException

# Gemini will be configured per request using database settings
GEMINI_AVAILABLE = False  # Will check per request


class AIService:
    """AI-powered features for syllabus management"""
    
    def __init__(self):
        self.syllabus_repo = SyllabusRepository()
        self.version_repo = SyllabusVersionRepository()
        self.clo_repo = CLORepository()
    
    def _get_gemini_model(self, db: Session):
        """Get Gemini model with API key from database or config"""
        try:
            # Try to get API key from database first
            api_key = SettingsService.get_gemini_api_key(db)
            
            if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
                return None
            
            genai.configure(api_key=api_key)
            return genai.GenerativeModel(settings.GEMINI_MODEL)
        except Exception as e:
            print(f"Gemini config error: {e}")
            return None
    
    def summarize(
        self, 
        db: Session, 
        syllabus_id: int, 
        language: str = "vi"
    ) -> SummarizeResponse:
        """
        AI auto-summarize syllabus content using Google Gemini
        Tóm tắt tự động nội dung giáo trình bằng Gemini AI
        """
        syllabus = self.syllabus_repo.get_by_id(db, syllabus_id)
        if not syllabus:
            raise HTTPException(status_code=404, detail="Syllabus not found")
        
        # Try Gemini AI first
        gemini_model = self._get_gemini_model(db)
        if gemini_model:
            try:
                return self._gemini_summarize(syllabus, language, gemini_model)
            except Exception as e:
                print(f"Gemini error, fallback to rule-based: {e}")
        
        # Fallback to rule-based
        return self._rule_based_summarize(syllabus, language)
    
    def _gemini_summarize(self, syllabus: Syllabus, language: str, model) -> SummarizeResponse:
        """Use Gemini AI for smart summarization"""
        prompt = f"""
Bạn là chuyên gia giáo dục. Hãy tóm tắt giáo trình sau đây bằng tiếng {language}:

Mã môn học: {syllabus.subject_code}
Tên môn học: {syllabus.subject_name}
Số tín chỉ: {syllabus.credits}
Mô tả: {syllabus.description or 'Không có'}
Mục tiêu: {syllabusives or 'Không có'}
Nội dung: {syllabus.content or 'Không có'}
Phương pháp giảng dạy: {syllabus.teaching_methods or 'Không có'}
Phương pháp đánh giá: {syllabus.assessment_methods or 'Không có'}

Yêu cầu:
1. Tóm tắt ngắn gọn (3-5 câu)
2. Liệt kê 3-5 điểm chính
3. Format: 
SUMMARY: [tóm tắt]
KEY_POINTS:
- [điểm 1]
- [điểm 2]
- [điểm 3]
"""
        
        response = model.generate_content(prompt)
        text = response.text
        
        # Parse response
        summary_part = ""
        key_points = []
        
        if "SUMMARY:" in text:
            parts = text.split("KEY_POINTS:")
            summary_part = parts[0].replace("SUMMARY:", "").strip()
            if len(parts) > 1:
                points_text = parts[1].strip()
                key_points = [line.strip("- ").strip() for line in points_text.split("\n") if line.strip().startswith("-")]
        else:
            summary_part = text
            key_points = ["AI-generated summary"]
        
        return SummarizeResponse(
            syllabus_id=syllabus.id,
            summary=summary_part,
            key_points=key_points,
            generated_at=datetime.utcnow()
        )
    
    def _rule_based_summarize(self, syllabus: Syllabus, language: str) -> SummarizeResponse:
        """Fallback rule-based summarization"""
        key_points = []
        
        if syllabus.objectives:
            key_points.append(f"Mục tiêu: {self._extract_first_sentence(syllabus.objectives)}")
        
        if syllabus.content:
            key_points.append(f"Nội dung: {self._extract_first_sentence(syllabus.content)}")
        
        if syllabus.assessment_methods:
            key_points.append(f"Đánh giá: {self._extract_first_sentence(syllabus.assessment_methods)}")
        
        summary = f"""
Giáo trình: {syllabus.subject_code} - {syllabus.subject_name}
Số tín chỉ: {syllabus.credits}
Học kỳ: {syllabus.semester}
Khoa: {syllabus.department}

Tóm tắt:
{syllabus.description or 'Chưa có mô tả'}

Phương pháp giảng dạy: {syllabus.teaching_methods or 'Chưa cập nhật'}
        """.strip()
        
        return SummarizeResponse(
            syllabus_id=syllabus.id,
            summary=summary,
            key_points=key_points,
            generated_at=datetime.utcnow()
        )
        
        if syllabus.assessment_methods:
            key_points.append(f"Đánh giá: {self._extract_first_sentence(syllabus.assessment_methods)}")
        
        # Generate summary
        summary = f"""
Giáo trình: {syllabus.subject_code} - {syllabus.subject_name}
Số tín chỉ: {syllabus.credits}
Học kỳ: {syllabus.semester}
Khoa: {syllabus.department}

Tóm tắt:
{syllabus.description or 'Chưa có mô tả'}

Phương pháp giảng dạy: {syllabus.teaching_methods or 'Chưa cập nhật'}
        """.strip()
        
        return SummarizeResponse(
            syllabus_id=syllabus_id,
            summary=summary,
            key_points=key_points,
            generated_at=datetime.utcnow()
        )
    
    def semantic_diff(
        self, 
        db: Session, 
        version_id_1: int, 
        version_id_2: int,
        language: str = "vi"
    ) -> DiffResponse:
        """
        AI semantic diff between two versions using Google Gemini
        So sánh ngữ nghĩa giữa 2 phiên bản bằng Gemini AI
        """
        v1 = self.version_repo.get_by_id(db, version_id_1)
        v2 = self.version_repo.get_by_id(db, version_id_2)
        
        if not v1 or not v2:
            raise HTTPException(status_code=404, detail="Version not found")
        
        if v1.syllabus_id != v2.syllabus_id:
            raise HTTPException(
                status_code=400, 
                detail="Versions must belong to the same syllabus"
            )
        
        # Try Gemini AI first
        gemini_model = self._get_gemini_model(db)
        if gemini_model:
            try:
                return self._gemini_diff(v1, v2, language, gemini_model)
            except Exception as e:
                print(f"Gemini diff error, fallback: {e}")
        
        # Fallback to rule-based
        return self._rule_based_diff(v1, v2)
    
    def _gemini_diff(self, v1: SyllabusVersion, v2: SyllabusVersion, language: str, model) -> DiffResponse:
        """Use Gemini AI for intelligent diff analysis"""
        prompt = f"""
Bạn là chuyên gia giáo dục. So sánh 2 phiên bản giáo trình và phân tích sự khác biệt:

PHIÊN BẢN {v1.version_number}:
Tên: {v1.subject_name}
Nội dung: {v1.content or 'Không có'}

PHIÊN BẢN {v2.version_number}:
Tên: {v2.subject_name}
Nội dung: {v2.content or 'Không có'}

Yêu cầu phân tích:
1. Tóm tắt các thay đổi
2. Phân loại: MAJOR (thay đổi lớn) hoặc MINOR (thay đổi nhỏ)
3. Đánh giá mức độ ảnh hưởng

Format trả về:
SUMMARY: [tóm tắt thay đổi]
MAJOR_CHANGES:
- [thay đổi lớn 1]
- [thay đổi lớn 2]
MINOR_CHANGES:
- [thay đổi nhỏ 1]
IMPACT: [Không ảnh hưởng/Ảnh hưởng vừa/Ảnh hưởng lớn]
"""
        
        response = gemini_model.generate_content(prompt)
        text = response.text
        
        # Parse response
        changes_summary = "AI analysis completed"
        major_changes = []
        minor_changes = []
        impact_analysis = "Cần review"
        
        if "SUMMARY:" in text:
            changes_summary = text.split("MAJOR_CHANGES:")[0].replace("SUMMARY:", "").strip()
        
        if "MAJOR_CHANGES:" in text and "MINOR_CHANGES:" in text:
            major_part = text.split("MAJOR_CHANGES:")[1].split("MINOR_CHANGES:")[0]
            major_changes = [{"field": "gemini_analysis", "description": line.strip("- ").strip()} 
                           for line in major_part.split("\n") if line.strip().startswith("-")]
            
            minor_part = text.split("MINOR_CHANGES:")[1].split("IMPACT:")[0]
            minor_changes = [{"field": "gemini_analysis", "description": line.strip("- ").strip()} 
                           for line in minor_part.split("\n") if line.strip().startswith("-")]
        
        if "IMPACT:" in text:
            impact_analysis = text.split("IMPACT:")[1].strip()
        
        return DiffResponse(
            version_1=v1.version_number,
            version_2=v2.version_number,
            changes_summary=changes_summary,
            major_changes=major_changes,
            minor_changes=minor_changes,
            impact_analysis=impact_analysis
        )
    
    def _rule_based_diff(self, v1: SyllabusVersion, v2: SyllabusVersion) -> DiffResponse:
        """Fallback rule-based diff"""
        major_changes = []
        minor_changes = []
        
        # Compare content
        if v1.content != v2.content:
            similarity = self._calculate_similarity(v1.content or "", v2.content or "")
            change = {
                "field": "content",
                "old_value": v1.content[:100] + "..." if v1.content and len(v1.content) > 100 else v1.content,
                "new_value": v2.content[:100] + "..." if v2.content and len(v2.content) > 100 else v2.content,
                "similarity": round(similarity, 2)
            }
            
            if similarity < 0.7:
                major_changes.append(change)
            else:
                minor_changes.append(change)
        
        # Compare subject name
        if v1.subject_name != v2.subject_name:
            major_changes.append({
                "field": "subject_name",
                "old_value": v1.subject_name,
                "new_value": v2.subject_name,
                "similarity": 0.0
            })
        
        # Generate summary
        changes_summary = f"Phát hiện {len(major_changes)} thay đổi lớn và {len(minor_changes)} thay đổi nhỏ"
        
        impact_analysis = "Thay đổi lớn" if len(major_changes) > 0 else "Thay đổi nhỏ"
        if len(major_changes) >= 3:
            impact_analysis = "Thay đổi rất lớn - cần review kỹ"
        
        return DiffResponse(
            version_1=v1.version_number,
            version_2=v2.version_number,
            changes_summary=changes_summary,
            major_changes=major_changes,
            minor_changes=minor_changes,
            impact_analysis=impact_analysis
        )
    
    def check_clo_similarity(
        self, 
        db: Session, 
        syllabus_id: int,
        clo_description: str
    ) -> CLOCheckResponse:
        """
        Check for similar CLOs across syllabuses using Google Gemini
        Gợi ý CLO tương tự từ các giáo trình khác bằng Gemini AI
        """
        # Get all CLOs except from current syllabus
        all_clos = db.query(CLO).filter(CLO.syllabus_id != syllabus_id).all()
        
        # Try Gemini AI for semantic similarity
        gemini_model = self._get_gemini_model(db)
        if gemini_model and all_clos:
            try:
                return self._gemini_clo_check(clo_description, all_clos, gemini_model)
            except Exception as e:
                print(f"Gemini CLO check error, fallback: {e}")
        
        # Fallback to rule-based
        return self._rule_based_clo_check(clo_description, all_clos)
    
    def _gemini_clo_check(self, clo_description: str, all_clos: List[CLO], model) -> CLOCheckResponse:
        """Use Gemini AI for semantic CLO matching"""
        # Prepare CLO list for prompt (limit to first 20 for token efficiency)
        clo_list = "\n".join([f"{i+1}. [{clo.id}] {clo.code}: {clo.description}" 
                             for i, clo in enumerate(all_clos[:20])])
        
        prompt = f"""
Bạn là chuyên gia giáo dục. Tìm các CLO (Course Learning Outcome) tương tự với CLO đầu vào.

CLO CẦN TÌM:
{clo_description}

DANH SÁCH CLO CÓ SẴN:
{clo_list}

Yêu cầu:
1. Tìm tối đa 5 CLO có nội dung tương tự
2. Đánh giá độ tương đồng từ 0.0 đến 1.0
3. Format trả về:
MATCHES:
[ID] - [Score] - [Lý do tương đồng]

Ví dụ:
MATCHES:
5 - 0.85 - Cùng về kỹ năng lập trình
"""
        
        response = model.generate_content(prompt)
        text = response.text
        
        suggestions = []
        if "MATCHES:" in text:
            matches_text = text.split("MATCHES:")[1].strip()
            for line in matches_text.split("\n"):
                if line.strip() and "-" in line:
                    try:
                        parts = line.split("-")
                        clo_id = int(parts[0].strip())
                        score = float(parts[1].strip())
                        
                        # Find CLO in list
                        clo = next((c for c in all_clos if c.id == clo_id), None)
                        if clo and score >= 0.5:
                            syllabus = self.syllabus_repo.get_by_id(db, clo.syllabus_id) if hasattr(self, 'syllabus_repo') else None
                            suggestions.append(CLOSuggestion(
                                clo_id=clo.id,
                                clo_code=clo.code,
                                description=clo.description,
                                similarity_score=round(score, 2),
                                syllabus_code=syllabus.subject_code if syllabus else "N/A",
                                syllabus_name=syllabus.subject_name if syllabus else "N/A"
                            ))
                    except (ValueError, IndexError):
                        continue
        
        suggestions.sort(key=lambda x: x.similarity_score, reverse=True)
        
        return CLOCheckResponse(
            input_clo=clo_description,
            suggestions=suggestions[:10],
            total_found=len(suggestions)
        )
    
    def _rule_based_clo_check(self, clo_description: str, all_clos: List[CLO]) -> CLOCheckResponse:
        """Fallback rule-based CLO similarity"""
        suggestions = []
        for clo in all_clos:
            similarity = self._calculate_similarity(
                clo_description.lower(), 
                clo.description.lower()
            )
            
            if similarity > 0.5:  # Threshold 50%
                syllabus = self.syllabus_repo.get_by_id(db, clo.syllabus_id) if hasattr(self, 'syllabus_repo') else None
                suggestions.append(CLOSuggestion(
                    clo_id=clo.id,
                    clo_code=clo.code,
                    description=clo.description,
                    similarity_score=round(similarity, 2),
                    syllabus_code=syllabus.subject_code if syllabus else "N/A",
                    syllabus_name=syllabus.subject_name if syllabus else "N/A"
                ))
        
        # Sort by similarity score
        suggestions.sort(key=lambda x: x.similarity_score, reverse=True)
        
        return CLOCheckResponse(
            input_clo=clo_description,
            suggestions=suggestions[:10],  # Top 10
            total_found=len(suggestions)
        )
    
    def _extract_first_sentence(self, text: str) -> str:
        """Extract first sentence from text"""
        if not text:
            return ""
        sentences = re.split(r'[.!?]', text)
        return sentences[0].strip() if sentences else text[:100]
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using SequenceMatcher"""
        if not text1 or not text2:
            return 0.0
        return SequenceMatcher(None, text1, text2).ratio()
