from django.contrib import admin
from django.urls import include, path
from .views import HealthCheckView
from .admin_views import LogDownloadView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "api/admin/logs/download/",
        LogDownloadView.as_view(),
        name="log-download",
    ),

    path(
        "api/health/",
        HealthCheckView.as_view(),
        name="health-check",
    ),

    path("api/", include("documents.urls")),
    path("api/", include("conversations.urls")),

    path("api/auth/", include("accounts.urls")),

    path(
        "api/auth/token/",
        TokenObtainPairView.as_view(),
        name="token-obtain-pair",
    ),
    path(
        "api/auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),
]