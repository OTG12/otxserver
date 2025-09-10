from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import FileSerializer

class FileUploadView(generics.CreateAPIView):
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser, FormParser]  # crucial for file uploads

    # permission_classes = [IsAuthenticatedOrReadOnly]  # adjust if you want open access
