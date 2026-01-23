from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io
from ..core.database import get_db
from ..models.user import User
from ..core.deps import get_current_user
from ..core.security import get_password_hash

router = APIRouter()

@router.post("/import")
async def import_users(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Import users from Excel file
    Required columns: email, full_name, password, role
    Optional columns: employee_id, degree, title, department, specialization, phone, 
                     office_location, research_interests, teaching_subjects, years_experience,
                     qualifications, publications, is_active
    """
    # Check if user is admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can import users"
        )
    
    # Check file extension
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only Excel files (.xlsx, .xls) are supported"
        )
    
    try:
        # Read Excel file
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Validate required columns
        required_columns = ['email', 'full_name', 'password', 'role']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required columns: {', '.join(missing_columns)}"
            )
        
        # Process users
        success_count = 0
        failed_users = []
        
        for index, row in df.iterrows():
            try:
                # Check if email already exists
                existing_user = db.query(User).filter(User.email == row['email']).first()
                if existing_user:
                    failed_users.append({
                        'row': index + 2,  # +2 because index starts at 0 and Excel has header
                        'email': row['email'],
                        'reason': 'Email already exists'
                    })
                    continue
                
                # Create user
                user_data = {
                    'email': row['email'],
                    'full_name': row['full_name'],
                    'hashed_password': get_password_hash(str(row['password'])),
                    'role': row['role'],
                    'is_active': bool(row.get('is_active', True))
                }
                
                # Add optional fields if present
                optional_fields = [
                    'employee_id', 'degree', 'title', 'department', 'specialization',
                    'phone', 'office_location', 'research_interests', 'teaching_subjects',
                    'years_experience', 'qualifications', 'publications'
                ]
                
                for field in optional_fields:
                    if field in df.columns and pd.notna(row[field]):
                        if field == 'years_experience':
                            user_data[field] = int(row[field])
                        else:
                            user_data[field] = str(row[field])
                
                new_user = User(**user_data)
                db.add(new_user)
                success_count += 1
                
            except Exception as e:
                failed_users.append({
                    'row': index + 2,
                    'email': row.get('email', 'N/A'),
                    'reason': str(e)
                })
        
        # Commit all successful users
        db.commit()
        
        return {
            'message': f'Import completed successfully',
            'total_rows': len(df),
            'success': success_count,
            'failed': len(failed_users),
            'failed_users': failed_users
        }
        
    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Excel file is empty"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )


@router.get("/template")
async def download_template(current_user: User = Depends(get_current_user)):
    """
    Download Excel template for user import
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can download template"
        )
    
    # Create sample DataFrame
    sample_data = {
        'email': ['lecturer1@smd.edu.vn', 'lecturer2@smd.edu.vn'],
        'full_name': ['Nguyễn Văn A', 'Trần Thị B'],
        'password': ['password123', 'password456'],
        'role': ['lecturer', 'lecturer'],
        'employee_id': ['GV001', 'GV002'],
        'degree': ['Tiến sĩ', 'Thạc sĩ'],
        'title': ['Giảng viên chính', 'Giảng viên'],
        'department': ['Khoa Công nghệ thông tin', 'Khoa Công nghệ thông tin'],
        'specialization': ['Machine Learning', 'Web Development'],
        'phone': ['+84901234567', '+84912345678'],
        'office_location': ['Phòng A101', 'Phòng A102'],
        'research_interests': ['AI, Machine Learning', 'Web Technologies'],
        'teaching_subjects': ['Python, Data Science', 'HTML, CSS, JavaScript'],
        'years_experience': [5, 3],
        'qualifications': ['PhD in Computer Science', 'MSc in Software Engineering'],
        'publications': ['10 papers', '5 papers'],
        'is_active': [True, True]
    }
    
    df = pd.DataFrame(sample_data)
    
    # Create Excel file in memory
    output = io.BytesIO()
    
    # Write to Excel
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Users')
    
    # Get the value and create new BytesIO for response
    excel_data = output.getvalue()
    
    from fastapi.responses import Response
    
    return Response(
        content=excel_data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=user_import_template.xlsx"
        }
    )
