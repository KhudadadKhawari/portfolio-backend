from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.content import BlogPost
from app.schemas.content import BlogPostCreate, BlogPostRead, BlogPostUpdate

router = APIRouter(prefix="/blog", tags=["blog"])
DbSession = Annotated[Session, Depends(get_db)]
AdminUser = Annotated[str, Depends(require_admin)]
BLOG_POST_NOT_FOUND = "Blog post not found"


@router.get("", response_model=list[BlogPostRead])
def list_posts(db: DbSession) -> list[BlogPost]:
    return list(
        db.scalars(select(BlogPost).where(BlogPost.published.is_(True)).order_by(BlogPost.id.desc()))
    )


@router.get("/{slug}", response_model=BlogPostRead)
def get_post(slug: str, db: DbSession) -> BlogPost:
    post = db.scalar(select(BlogPost).where(BlogPost.slug == slug))
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=BLOG_POST_NOT_FOUND)
    return post


@router.post("", response_model=BlogPostRead, status_code=status.HTTP_201_CREATED)
def create_post(
    payload: BlogPostCreate,
    db: DbSession,
    _: AdminUser,
) -> BlogPost:
    post = BlogPost(**payload.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.put("/{post_id}", response_model=BlogPostRead)
def update_post(
    post_id: int,
    payload: BlogPostUpdate,
    db: DbSession,
    _: AdminUser,
) -> BlogPost:
    post = db.get(BlogPost, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=BLOG_POST_NOT_FOUND)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: DbSession,
    _: AdminUser,
) -> None:
    post = db.get(BlogPost, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=BLOG_POST_NOT_FOUND)
    db.delete(post)
    db.commit()
