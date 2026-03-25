from django.urls import path

from apps.integrations.views import SuggestedTaskTitleView


urlpatterns = [
    path("suggested-task-title/", SuggestedTaskTitleView.as_view(), name="suggested-task-title"),
]
