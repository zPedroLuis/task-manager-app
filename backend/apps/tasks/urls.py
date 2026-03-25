from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.tasks.views import CategoryViewSet, TaskViewSet


router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("", include(router.urls)),
]
