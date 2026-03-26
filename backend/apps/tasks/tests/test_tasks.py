import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.tasks.models import Category, Task


@pytest.fixture
def user():
    return User.objects.create_user(username="owner", password="senha12345")


@pytest.fixture
def other_user():
    return User.objects.create_user(username="guest", password="senha12345")


@pytest.fixture
def auth_client(user):
    client = APIClient()
    response = client.post(
        "/api/auth/login/",
        {"username": "owner", "password": "senha12345"},
        format="json",
    )
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    return client


@pytest.mark.django_db
def test_create_task(auth_client, user):
    category = Category.objects.create(name="Trabalho", owner=user)

    response = auth_client.post(
        "/api/tasks/",
        {"title": "Finalizar relatório", "category": category.id},
        format="json",
    )

    assert response.status_code == 201
    assert Task.objects.filter(title="Finalizar relatório", owner=user).exists()


@pytest.mark.django_db
def test_filter_tasks_by_completed(auth_client, user):
    Task.objects.create(title="Tarefa aberta", owner=user, completed=False)
    Task.objects.create(title="Tarefa finalizada", owner=user, completed=True)

    response = auth_client.get("/api/tasks/?completed=true")

    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["title"] == "Tarefa finalizada"


@pytest.mark.django_db
def test_share_task_with_another_user(auth_client, user, other_user):
    task = Task.objects.create(title="Compartilhar demo", owner=user)

    response = auth_client.patch(
        f"/api/tasks/{task.id}/",
        {"shared_with": [other_user.id]},
        format="json",
    )

    task.refresh_from_db()
    assert response.status_code == 200
    assert task.shared_with.filter(id=other_user.id).exists()
