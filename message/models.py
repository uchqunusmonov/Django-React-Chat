from django.db import models


class GenericFileUpload(models.Model):
    file_upload = models.FileField(upload_to='images')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_date}"
