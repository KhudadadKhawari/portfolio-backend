from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.content import Project
from app.schemas.content import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])
DbSession = Annotated[Session, Depends(get_db)]
AdminUser = Annotated[str, Depends(require_admin)]
PROJECT_NOT_FOUND = "Project not found"
PROJECT_SLUG_EXISTS = "Project slug already exists"


def ensure_project_slug_available(db: Session, slug: str, project_id: int | None = None) -> None:
    existing_project = db.scalar(select(Project).where(Project.slug == slug))
    if existing_project is not None and existing_project.id != project_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=PROJECT_SLUG_EXISTS)


@router.get("", response_model=list[ProjectRead])
def list_projects(db: DbSession) -> list[Project]:
    return list(
        db.scalars(select(Project).options(selectinload(Project.assets)).order_by(Project.id.desc()))
    )


@router.get("/{slug}", response_model=ProjectRead)
def get_project(slug: str, db: DbSession) -> Project:
    project = db.scalar(
        select(Project).options(selectinload(Project.assets)).where(Project.slug == slug)
    )
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PROJECT_NOT_FOUND)
    return project


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    db: DbSession,
    _: AdminUser,
) -> Project:
    ensure_project_slug_available(db, payload.slug)
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.put("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: DbSession,
    _: AdminUser,
) -> Project:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PROJECT_NOT_FOUND)
    if payload.slug is not None:
        ensure_project_slug_available(db, payload.slug, project_id=project.id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: DbSession,
    _: AdminUser,
) -> None:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PROJECT_NOT_FOUND)
    db.delete(project)
    db.commit()
