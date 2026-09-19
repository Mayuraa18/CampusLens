from django.urls import path

from .views import (
    DocumentDetailView,
    DocumentInsightsView,
    DocumentListView,
)

urlpatterns = [
    path(
        "documents/",
        DocumentListView.as_view(),
        name="document-list",
    ),
    path(
        "documents/<int:pk>/",
        DocumentDetailView.as_view(),
        name="document-detail",
    ),
    path(
        "documents/<int:pk>/insights/",
        DocumentInsightsView.as_view(),
        name="document-insights",
    ),
]