from fastapi import FastAPI
from core.exceptions import setup_exception_handlers, NotFoundException, BadRequestException
from datetime import datetime
from database.db import Base, engine
from models.club import Club
from models.club_activity import ClubActivity
from models.club_member import ClubMember
from models.user import User
from models.activity_log import ActivityLog
from routers.auth_router import router_auth
from routers.users_router import router_user
from routers.club_router import router_club
from routers.club_member_router import router_club_member
from routers.club_activity_router import router_activities

Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_club)
app.include_router(router_activities)
app.include_router(router_club_member)

setup_exception_handlers(app)

@app.get("/test")
def health_check():
    return {
        "status": "success",
        "message": "Service dang chay",
        "timestamp": datetime.now().isoformat()
    }

