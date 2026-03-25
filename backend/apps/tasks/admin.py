from django.contrib import admin

from apps.tasks.models import Category, Task


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "created_at")
    search_fields = ("name", "owner__username")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "completed", "category", "created_at")
    list_filter = ("completed", "category")
    search_fields = ("title", "description", "owner__username")
