from fastapi import FastAPI
from .core.database import engine, Base

# Import all routers
from .api.v1 import auth as auth_router
from .api.v1 import user as user_router
from .api.v1 import syllabus as syllabus_router
from .api.v1 import workflow as workflow_router
from .api.v1 import review as review_router
from .api.v1 import clo_plo as clo_plo_router
from .api.v1 import search as search_router


Base.metadata.create_all(bind=engine)  # Create tables


app = FastAPI(
    title="SMD Backend - Syllabus Management System",
    description="Backend API for Syllabus Management & Digitalization System"
)

@app.get("/")
def root():
    return {"message": "Syllabus Management API", "status": "running"}

@app.get("/test")
def test_endpoint():
    return {"message": "Test endpoint working", "status": "success"}

# Include all routers
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(syllabus_router.router)
app.include_router(workflow_router.router)
app.include_router(review_router.router)
app.include_router(clo_plo_router.router)
app.include_router(search_router.router)
