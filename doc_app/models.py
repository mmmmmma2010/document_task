from django.db import models

# Create your models here.
class UploadedFile(models.Model):
    FILE_TYPES = (
        ('image', 'Image'),
        ('pdf', 'PDF'),
    )

    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)

    