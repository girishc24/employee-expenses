# validators.py
from django.core.exceptions import ValidationError

def validate_file_size(value):
    filesize = value.size

    if filesize > 52428800:  # 50MB limit
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value
