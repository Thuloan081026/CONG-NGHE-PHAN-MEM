from fastapi import FastAPI
from .core.database import engine, Base

from .api.v1 import auth as auth_router
from .api.v1 import user as user_router
from .api.v1 import syllabus as syllabus_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="SMD Backend - Syllabus Management System",
    description="Backend API for Syllabus Management & Digitalization System"
)

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(syllabus_router.router)
