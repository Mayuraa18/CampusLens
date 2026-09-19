from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Document
from .serializers import (
    DocumentDetailSerializer,
    DocumentSerializer,
    InsightsSerializer,
)
from .services.document_processor import process_document
from .services.insights import generate_document_insights


class DocumentListView(APIView):
    def get(self, request):
        documents = Document.objects.filter(
            user=request.user,
        )

        serializer = DocumentSerializer(
            documents,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentSerializer(
            data=request.data,
        )

        if serializer.is_valid():
            document = serializer.save(
                user=request.user,
            )

            try:
                process_document(document)
            except Exception:
                return Response(
                    {
                        "detail": (
                            "Document was uploaded, "
                            "but processing failed."
                        )
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            document.refresh_from_db()

            return Response(
                DocumentSerializer(document).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class DocumentDetailView(APIView):
    def get(self, request, pk):
        try:
            document = Document.objects.get(
                pk=pk,
                user=request.user,
            )
        except Document.DoesNotExist:
            return Response(
                {"detail": "Document not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DocumentDetailSerializer(
            document,
        )

        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            document = Document.objects.get(
                pk=pk,
                user=request.user,
            )
        except Document.DoesNotExist:
            return Response(
                {"detail": "Document not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        document.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class DocumentInsightsView(APIView):
    def get(self, request, pk):
        try:
            document = Document.objects.get(
                pk=pk,
                user=request.user,
            )
        except Document.DoesNotExist:
            return Response(
                {"detail": "Document not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if document.status != Document.Status.PROCESSED:
            return Response(
                {
                    "detail": (
                        "Insights are not available because "
                        "the document has not finished processing."
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )

        insights = generate_document_insights(document)

        serializer = InsightsSerializer(
            insights,
        )

        return Response(serializer.data)