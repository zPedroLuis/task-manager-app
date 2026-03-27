import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_register_user():
    client = APIClient()
    payload = {
        "username": "pedro",
        "email": "pedro@example.com",
        "password": "senha12345",
    }

    response = client.post("/api/auth/register/", payload, format="json")

    assert response.status_code == 201
    assert User.objects.filter(username="pedro").exists()


@pytest.mark.django_db
def test_login_user_returns_tokens():
    User.objects.create_user(username="pedro", email="pedro@example.com", password="senha12345")
    client = APIClient()

    response = client.post(
        "/api/auth/login/",
        {"username": "pedro", "password": "senha12345"},
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_users_list_authenticated():
    User.objects.create_user(username="owner", password="senha12345")
    User.objects.create_user(username="guest", password="senha12345")
    client = APIClient()
    token_response = client.post(
        "/api/auth/login/",
        {"username": "owner", "password": "senha12345"},
        format="json",
    )
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}")

    response = client.get("/api/auth/users/")

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["username"] == "guest"
