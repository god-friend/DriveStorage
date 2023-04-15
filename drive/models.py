from django.db import models
from django.contrib.auth.models import User
import os

def uploadTo(instance, filename):
    if instance.path != '' and instance.path != '/':
        return str(instance.user.username)+instance.path + filename
    return str(instance.user.username)+'/'+filename

class UploadedFiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(blank=True, upload_to=uploadTo)
    upload_time = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True)
    path = models.CharField(max_length=256, default='')

    def filename(self):
        return os.path.basename(self.file.name)
    
    def get_full_url(self):
        return self.link

    def __str__(self):
        if self.path:
            return self.path+self.filename()
        return self.filename()