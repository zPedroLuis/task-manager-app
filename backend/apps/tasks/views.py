from django.db.models import Q
from rest_framework import viewsets

from apps.tasks.models import Category, Task
from apps.tasks.permissions import IsOwnerOrSharedReadOnly
from apps.tasks.serializers import CategorySerializer, TaskSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = (IsOwnerOrSharedReadOnly,)
    filterset_fields = ("completed", "category")
    search_fields = ("title", "description")
    ordering_fields = ("created_at", "updated_at", "due_date")

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(Q(owner=user) | Q(shared_with=user)).distinct().prefetch_related("shared_with")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
