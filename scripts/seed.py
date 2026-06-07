from app.db.session import SessionLocal
from app.models.content import BlogPost, Certification, Project


def main() -> None:
    with SessionLocal() as db:
        if not db.query(Project).first():
            db.add(
                Project(
                    title="CI/CD Portfolio Platform",
                    slug="ci-cd-portfolio-platform",
                    summary="A portfolio application built to teach GitHub Actions deployments.",
                    description=(
                        "FastAPI, Next.js, PostgreSQL, MinIO, Docker Compose, and Docker Hub."
                    ),
                    repository_url="https://github.com/example/portfolio-backend",
                    live_url="https://example.com",
                    tags=["FastAPI", "Next.js", "Docker", "GitHub Actions"],
                    featured=True,
                )
            )
        if not db.query(BlogPost).first():
            db.add(
                BlogPost(
                    title="How This Deployment Pipeline Works",
                    slug="how-this-deployment-pipeline-works",
                    excerpt=(
                        "A short walkthrough of lint, tests, scans, image build, deploy, "
                        "and health checks."
                    ),
                    content=(
                        "This demo shows the flow from pull request checks to production "
                        "deployment on a VPS."
                    ),
                    published=True,
                )
            )
        if not db.query(Certification).first():
            db.add(
                Certification(
                    name="DevOps Bootcamp Demo Certificate",
                    issuer="Demo Academy",
                    issued_at="2026-06",
                    credential_url="https://example.com/certificates/demo",
                    description="Sample certification record for the portfolio demo.",
                )
            )
        db.commit()


if __name__ == "__main__":
    main()
