from django.db import models
from django.dispatch import receiver
import os

class UserFile(models.Model):
    id = models.UUIDField(primary_key=True)
    file = models.FileField(upload_to="data")
    accesspwd = models.CharField(max_length=255)
    deletionpwd = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)


@receiver(models.signals.post_delete, sender=UserFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
