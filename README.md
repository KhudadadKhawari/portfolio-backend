# Portfolio Backend

FastAPI backend for the portfolio CI/CD demo. It provides public portfolio APIs, admin-only content management, file uploads to MinIO, PostgreSQL persistence, tests, Docker, and GitHub Actions.

## Features

- Health endpoint at `/health` and `/api/health`
- JWT admin login at `/api/v1/auth/login`
- Projects CRUD at `/api/v1/projects`
- Blog CRUD at `/api/v1/blog`
- Certifications CRUD at `/api/v1/certifications`
- Admin-only uploads at `/api/v1/uploads`
- PostgreSQL via SQLAlchemy and Alembic
- MinIO-compatible object storage via boto3

## Local Setup

```bash
cp .env.example .env
docker compose up -d postgres minio
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
python scripts/seed.py
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` for OpenAPI docs.

## Docker Development

```bash
cp .env.example .env
docker compose up --build
```

Run migrations inside the backend container:

```bash
docker compose exec backend alembic upgrade head
docker compose exec backend python scripts/seed.py
```

## Tests and Quality

```bash
ruff check .
pytest
pip-audit
```

## CI/CD Demo

The GitHub Actions workflow lints, tests, scans with self-hosted SonarQube, runs dependency and image security checks, builds a Docker image, pushes it to Docker Hub, deploys over SSH, runs a health check, and sends a generic webhook notification.

Required secrets:

- `VPS_HOST`
- `VPS_USER`
- `VPS_PORT`
- `VPS_SSH_KEY`
- `SONAR_HOST_URL`
- `SONAR_TOKEN`
- `DEPLOY_WEBHOOK_URL`
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
