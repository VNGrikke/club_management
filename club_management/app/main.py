from fastapi import FastAPI
from core.exceptions import setup_exception_handlers, NotFoundException, BadRequestException
from datetime import datetime
from database.db import Base, engine
from models.club import Club
from models.club_activity import ClubActivity
from models.club_member import ClubMember
from models.user import User
from club_management.app.routers.auth_router import router_auth


Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(router_auth)

setup_exception_handlers(app)

@app.get("/test")
def health_check():
    return {
        "status": "success",
        "message": "Service dang chay",
        "timestamp": datetime.now().isoformat()
    }

