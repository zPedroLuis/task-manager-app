import requests
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


class SuggestedTaskTitleView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        category = request.query_params.get("category", "geral")
        base_url = settings.EXTERNAL_API_BASE_URL.rstrip("/")
        endpoint = f"{base_url}/tips"

        try:
            response = requests.get(endpoint, params={"category": category}, timeout=5)
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException:
            return Response(
                {"detail": "Falha ao consultar API externa."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            {
                "category": category,
                "suggested_title": payload.get("title", "Organizar tarefas do dia"),
                "source": "external-api",
            }
        )
