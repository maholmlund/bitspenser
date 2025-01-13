from django.db import models

class UserFile(models.Model):
    name = models.UUIDField
    file = models.FileField(upload_to="data")
    accesspwd = models.CharField(max_length=255)
    deletionpwd = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
