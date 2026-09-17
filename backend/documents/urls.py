from django.urls import path

from .views import DocumentDetailView, DocumentListView

urlpatterns = [
    path("documents/", DocumentListView.as_view(), name="document-list"),
    path(
        "documents/<int:pk>/",
        DocumentDetailView.as_view(),
        name="document-detail",
    ),
]