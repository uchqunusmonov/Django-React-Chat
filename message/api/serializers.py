from rest_framework import serializers
from message.models import GenericFileUpload


class GenericFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericFileUpload
        fields = "__all__"