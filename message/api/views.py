from rest_framework.viewsets import ModelViewSet
from .serializers import GenericFileUploadSerializer
from message.models import GenericFileUpload


class GenericFileUploadView(ModelViewSet):
    queryset = GenericFileUpload.objects.all()
    serializer_class = GenericFileUploadSerializer