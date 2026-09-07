from models.activity_log import ActivityLog
from sqlalchemy.orm import Session
 
def log_activity(db: Session, action: str, user_id: int, target_id: int = None, details: str = ""):
    new_log = ActivityLog(
        user_id=user_id,
        action=action,
        target_id=target_id,
        details=details
    )
    db.add(new_log)
    db.commit()