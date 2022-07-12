from rest_framework.viewsets import ModelViewSet
from .serializers import GenericFileUploadSerializer, MessageSerializer, MessageAttachmentSerializer
from message.models import GenericFileUpload, Message, MessageAttachment
from rest_framework.response import Response
from rest_framework import status
from config.custom_methods import IsAthenticatedCustom
from django.db.models import Q
from config.settings import SOCKET_SERVER
import requests
import json


def handleRequest(serializerData):
    notification = {
            "message": serializerData.data.get("message"),
            "from": serializerData.data.get("sender"),
            "receiver": serializerData.data.get("receiver").get("id")
        }
    headers = {
        'Content-Type': 'application/json',
    }
    try:
        requests.post(SOCKET_SERVER, json.dumps(notification), headers=headers)
    except Exception as e:
        pass
    return True


class GenericFileUploadView(ModelViewSet):
    queryset = GenericFileUpload.objects.all()
    serializer_class = GenericFileUploadSerializer


class MessageView(ModelViewSet):
    queryset = Message.objects.select_related("sender", "receiver").prefetch_related("message_attachments")
    serializer_class = MessageSerializer
    permission_classes = (IsAthenticatedCustom,)

    def get_queryset(self):
        data = self.request.query_params.dict()
        user_id = data.get("user_id", None)

        if user_id:
            active_user_id = self.request.user.id
            return self.queryset.filter(Q(sender_id=user_id, receiver_id=active_user_id)|Q(sender_id=active_user_id,receiver_id=user_id)).distinct()

        return self.queryset

    def create(self, request, *args, **kwargs):
        try:
            request.data._mutable = True
        except:
            pass
        attachments = request.data.pop("attachments", None)
        if str(request.user.id) != str(request.data.get("sender_id", None)):
            raise Exception("only sender can create a message")

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if attachments:
            MessageAttachment.objects.bulk_create([MessageAttachment(**attachment, message_id=serializer.data["id"]) for attachment in attachments])
            message_data = self.get_queryset().get(id=serializer.data['id'])
            return Response(self.serializer_class(message_data).data, status=status.HTTP_201_CREATED)
        
        try:
            handleRequest(serializer)
        except:
            pass

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        try:
            request.data._mutable = True
        except:
            pass
        attachments = request.data.pop("attachments", None)
        instance = self.get_object()
        serializer = self.serializer_class(data=request.data, instance=instance, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        MessageAttachment.objects.filter(message_id=instance.id).delete()

        if attachments:
            MessageAttachment.objects.bulk_create([MessageAttachment(**attachment, message_id=instance.id) for attachment in attachments])
            message_data = self.get_object()
            return Response(self.serializer_class(message_data).data, status=status.HTTP_200_OK)
        try:
            handleRequest(serializer)
        except:
            pass
        return Response(serializer.data, status=status.HTTP_200_OK)





