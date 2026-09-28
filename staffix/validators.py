"""Reusable upload validators (file size + file type) for photo/document fields.

Usage in a model:

    from django.db import models
    from staffix.validators import validate_upload_size, validate_upload_extension

    class Employee(models.Model):
        photo = models.FileField(
            upload_to='photos/',
            validators=[validate_upload_size, validate_upload_extension],
        )
"""

import os

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_upload_size(file):
    """Reject files bigger than settings.MAX_UPLOAD_SIZE (default 4 MB)."""
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 1024 * 1024 * 4)
    if file.size > max_size:
        raise ValidationError(
            'File too large. Size should not exceed %.1f MB.' % (max_size / (1024 * 1024))
        )


def validate_upload_extension(file):
    """Only allow file extensions listed in settings.ALLOWED_UPLOAD_EXTENSIONS."""
    allowed_extensions = getattr(settings, 'ALLOWED_UPLOAD_EXTENSIONS', ['pdf', 'png', 'jpg', 'jpeg'])
    ext = os.path.splitext(file.name)[1].lower().lstrip('.')
    if ext not in allowed_extensions:
        raise ValidationError(
            'Unsupported file type "%s". Allowed types: %s.' % (ext, ', '.join(allowed_extensions))
        )
