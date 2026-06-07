def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_public_content_lists(client):
    assert client.get("/api/v1/projects").status_code == 200
    assert client.get("/api/v1/blog").status_code == 200
    assert client.get("/api/v1/certifications").status_code == 200


def test_login_rejects_bad_password(client):
    response = client.post("/api/v1/auth/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401


def test_admin_can_create_project(client, admin_token):
    response = client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "title": "New Project",
            "slug": "new-project",
            "summary": "New summary",
            "description": "New description",
            "tags": ["fastapi"],
            "featured": True,
        },
    )
    assert response.status_code == 201
    assert response.json()["slug"] == "new-project"


def test_admin_required_for_writes(client):
    response = client.post(
        "/api/v1/blog",
        json={
            "title": "Blocked",
            "slug": "blocked",
            "excerpt": "Blocked",
            "content": "Blocked",
            "published": True,
        },
    )
    assert response.status_code == 403
