import logging

from django.http import JsonResponse
from django.views import View

logger = logging.getLogger("campuslens")


class HealthCheckView(View):
    def get(self, request):
        logger.info("Health check requested")

        return JsonResponse({
            "status": "ok",
            "service": "CampusLens API",
        })