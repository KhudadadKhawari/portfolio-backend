from fastapi import APIRouter

from app.api.routes import auth, blog, certifications, projects, uploads

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(projects.router)
api_router.include_router(blog.router)
api_router.include_router(certifications.router)
api_router.include_router(uploads.router)
