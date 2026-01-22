"""
Audit Log API endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
from datetime import datetime, date

from ...core.database import get_db
from ...core.deps import require_roles
from ...models.user import User

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs (Admin Only)"])


@router.get("/")
def get_audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    action: Optional[str] = None,
    role: Optional[str] = None,
    status: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    """
    Get audit logs with filtering and pagination (Admin only)
    """
    # Build base query
    query = """
        SELECT 
            id,
            timestamp,
            user_id,
            user_email,
            user_role,
            action,
            details,
            status,
            ip_address
        FROM audit_logs
        WHERE 1=1
    """
    params = {}
    
    # Apply filters
    if action:
        query += " AND action = :action"
        params['action'] = action
    
    if role:
        query += " AND user_role = :role"
        params['role'] = role
    
    if status:
        query += " AND status = :status"
        params['status'] = status
    
    if date_from:
        query += " AND DATE(timestamp) >= :date_from"
        params['date_from'] = date_from
    
    if date_to:
        query += " AND DATE(timestamp) <= :date_to"
        params['date_to'] = date_to
    
    if search:
        query += """ AND (
            user_email LIKE :search 
            OR action LIKE :search 
            OR details LIKE :search
        )"""
        params['search'] = f"%{search}%"
    
    # Count total
    count_query = f"SELECT COUNT(*) as total FROM ({query}) as filtered"
    total_result = db.execute(text(count_query), params).fetchone()
    total = total_result[0] if total_result else 0
    
    # Add sorting and pagination
    query += " ORDER BY timestamp DESC"
    query += " LIMIT :limit OFFSET :offset"
    params['limit'] = page_size
    params['offset'] = (page - 1) * page_size
    
    # Execute query
    result = db.execute(text(query), params)
    logs = []
    
    for row in result:
        logs.append({
            'id': row[0],
            'timestamp': row[1].isoformat() if row[1] else None,
            'user_id': row[2],
            'user': row[3],
            'role': row[4],
            'action': row[5],
            'details': row[6],
            'status': row[7],
            'ip': row[8]
        })
    
    return {
        'total': total,
        'count': len(logs),
        'page': page,
        'page_size': page_size,
        'items': logs
    }


@router.get("/stats")
def get_audit_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    """
    Get audit log statistics (Admin only)
    """
    stats_query = text("""
        SELECT 
            COUNT(*) as total_logs,
            COUNT(DISTINCT user_email) as unique_users,
            SUM(CASE WHEN DATE(timestamp) = CURDATE() THEN 1 ELSE 0 END) as today_logs,
            SUM(CASE WHEN timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR) THEN 1 ELSE 0 END) as last_24h_users,
            SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed_actions
        FROM audit_logs
    """)
    
    result = db.execute(stats_query).fetchone()
    
    return {
        'total_logs': result[0] or 0,
        'unique_users': result[1] or 0,
        'today_logs': result[2] or 0,
        'active_users_24h': result[3] or 0,
        'failed_actions': result[4] or 0
    }


@router.get("/actions")
def get_action_breakdown(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    """
    Get breakdown of actions (Admin only)
    """
    query = text("""
        SELECT action, COUNT(*) as count
        FROM audit_logs
        GROUP BY action
        ORDER BY count DESC
    """)
    
    result = db.execute(query)
    actions = []
    
    for row in result:
        actions.append({
            'action': row[0],
            'count': row[1]
        })
    
    return actions
