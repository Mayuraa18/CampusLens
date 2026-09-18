import logging
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView


logger = logging.getLogger("campuslens")


class LogDownloadView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        log_path = Path(settings.BASE_DIR) / "logs" / "campuslens.log"

        if not log_path.exists():
            raise Http404("Log file does not exist.")

        logger.info(
            "Log file downloaded by admin user %s",
            request.user.username,
        )

        return FileResponse(
            open(log_path, "rb"),
            as_attachment=True,
            filename="campuslens.log",
        )