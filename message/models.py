from django.db import models


class GenericFileUpload(models.Model):
    file_upload = models.FileField(upload_to='images')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_date}"


class Message(models.Model):
    sender = models.ForeignKey('users.CustomUser', related_name='message_sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey('users.CustomUser', related_name='message_receiver', on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"message between {self.sender.name} and {self.receiver.name}"

    class Meta:
        ordering = ['-created_date',]


class MessageAttachment(models.Model):
    message = models.ForeignKey(Message, related_name="message_attachments", on_delete=models.CASCADE)
    attachment = models.ForeignKey(GenericFileUpload, related_name="message_uploads", on_delete=models.CASCADE)
    caption = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption

    class Meta:
        ordering = ['created_date',]

