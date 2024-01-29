from django.db import models
from django.core.exceptions import ValidationError
import os


def validate_docx_file(value):
    ext = os.path.splitext(value.name)[1]  # Extracts the extension from the filename
    valid_extensions = ['.docx']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Only docx files are allowed.')


class Document(models.Model):
    original_doc = models.FileField(upload_to='originals/', validators=[validate_docx_file])
    translated_doc = models.FileField(upload_to='translations/', validators=[validate_docx_file])

    def __str__(self):
        return f"Document {self.id}"


from django.db import models

# Create your models here.
