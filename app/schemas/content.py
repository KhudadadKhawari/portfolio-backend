from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class AssetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    object_key: str
    file_name: str
    content_type: str
    size_bytes: int
    category: str
    url: str
    created_at: datetime


class ProjectBase(BaseModel):
    title: str = Field(min_length=2, max_length=160)
    slug: str = Field(min_length=2, max_length=180)
    summary: str = Field(min_length=2, max_length=320)
    description: str = Field(min_length=2)
    repository_url: str | None = None
    live_url: str | None = None
    tags: list[str] = []
    featured: bool = False


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    summary: str | None = None
    description: str | None = None
    repository_url: str | None = None
    live_url: str | None = None
    tags: list[str] | None = None
    featured: bool | None = None


class ProjectRead(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    assets: list[AssetRead] = []
    created_at: datetime
    updated_at: datetime


class BlogPostBase(BaseModel):
    title: str = Field(min_length=2, max_length=180)
    slug: str = Field(min_length=2, max_length=200)
    excerpt: str = Field(min_length=2, max_length=360)
    content: str = Field(min_length=2)
    published: bool = True


class BlogPostCreate(BlogPostBase):
    pass


class BlogPostUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    excerpt: str | None = None
    content: str | None = None
    published: bool | None = None


class BlogPostRead(BlogPostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class CertificationBase(BaseModel):
    name: str = Field(min_length=2, max_length=180)
    issuer: str = Field(min_length=2, max_length=180)
    issued_at: str | None = None
    credential_url: str | None = None
    description: str | None = None


class CertificationCreate(CertificationBase):
    pass


class CertificationUpdate(BaseModel):
    name: str | None = None
    issuer: str | None = None
    issued_at: str | None = None
    credential_url: str | None = None
    description: str | None = None


class CertificationRead(CertificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    assets: list[AssetRead] = []
    created_at: datetime
    updated_at: datetime
