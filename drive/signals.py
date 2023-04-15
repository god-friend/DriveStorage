from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save
import os
from .models import UploadedFiles

@receiver(post_save, sender=User)
def make_dir(sender, instance, created, **kwargs):
    if not os.path.exists('media/'+str(instance.username)) and not instance.is_superuser:
        os.mkdir('media/'+str(instance.username))


@receiver(post_delete, sender=UploadedFiles)
def delete_from_storage(sender, instance, **kwargs):
    os.remove('media/'+str(instance.file))
