from django.contrib.auth.models import User
from rest_framework import serializers

from apps.tasks.models import Category, Task


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "created_at")
        read_only_fields = ("id", "created_at")


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    shared_with = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        queryset=User.objects.all(),
    )

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "completed",
            "due_date",
            "owner",
            "category",
            "shared_with",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "owner", "created_at", "updated_at")

    def validate_category(self, value):
        if value and value.owner != self.context["request"].user:
            raise serializers.ValidationError("Categoria inválida para este usuário.")
        return value

    def validate_shared_with(self, users):
        request_user = self.context["request"].user
        for user in users:
            if user == request_user:
                raise serializers.ValidationError("Não compartilhe tarefa com o próprio usuário.")
        return users
