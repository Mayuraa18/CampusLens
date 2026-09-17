from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Document
from .serializers import DocumentSerializer


class DocumentListView(APIView):
    def get(self, request):
        documents = Document.objects.filter(user=request.user)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

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
                status=404,
            )

        serializer = DocumentSerializer(document)
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
                status=404,
            )

        document.delete()
        return Response(status=204)