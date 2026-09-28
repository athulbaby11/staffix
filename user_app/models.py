import os

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

from admin_app.models import Job

# Maximum allowed size for a passport upload (3 MB).
MAX_PASSPORT_UPLOAD_SIZE = 1024 * 1024 * 3
ALLOWED_PASSPORT_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png']

phone_number_validator = RegexValidator(
    regex=r'^\+?[0-9 ]{7,15}$',
    message='Enter a valid phone number (7-15 digits, optionally starting with +).',
)

ni_number_validator = RegexValidator(
    regex=r'^[A-Za-z]{2}[0-9]{6}[A-Za-z]$',
    message='Enter a valid National Insurance number, e.g. QQ123456C.',
)

zip_code_validator = RegexValidator(
    regex=r'^[A-Za-z0-9 ]{3,10}$',
    message='Enter a valid zip/postal code.',
)

# Maximum allowed size for general employee document uploads (3 MB).
MAX_DOCUMENT_UPLOAD_SIZE = 1024 * 1024 * 3
ALLOWED_DOCUMENT_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png']
ALLOWED_PHOTO_EXTENSIONS = ['jpg', 'jpeg', 'png']


def validate_document_size(file):
    """Reject document uploads bigger than 3 MB."""
    if file.size > MAX_DOCUMENT_UPLOAD_SIZE:
        raise ValidationError('File too large. Size should not exceed 3 MB.')


def validate_document_extension(file):
    """Only allow PDF/JPEG/PNG document uploads."""
    ext = os.path.splitext(file.name)[1].lower().lstrip('.')
    if ext not in ALLOWED_DOCUMENT_EXTENSIONS:
        raise ValidationError(
            'Unsupported file type "%s". Allowed types: PDF, JPEG, PNG.' % ext
        )


def validate_photo_extension(file):
    """Only allow JPEG/PNG photo uploads (no PDF)."""
    ext = os.path.splitext(file.name)[1].lower().lstrip('.')
    if ext not in ALLOWED_PHOTO_EXTENSIONS:
        raise ValidationError(
            'Unsupported file type "%s". Allowed types: JPEG, PNG.' % ext
        )


def validate_passport_size(file):
    """Reject passport uploads bigger than 3 MB."""
    if file.size > MAX_PASSPORT_UPLOAD_SIZE:
        raise ValidationError('File too large. Size should not exceed 3 MB.')


def validate_passport_extension(file):
    """Only allow PDF/JPEG/PNG passport uploads."""
    ext = os.path.splitext(file.name)[1].lower().lstrip('.')
    if ext not in ALLOWED_PASSPORT_EXTENSIONS:
        raise ValidationError(
            'Unsupported file type "%s". Allowed types: PDF, JPEG, PNG.' % ext
        )


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, validators=[phone_number_validator])
    ni_number = models.CharField(max_length=13, validators=[ni_number_validator])
    address = models.TextField()
    zip_code = models.CharField(max_length=10, verbose_name='Zip code', validators=[zip_code_validator])
    dob = models.DateField(verbose_name='Date of birth')
    passport = models.FileField(
        upload_to='applications/passports/',
        validators=[validate_passport_size, validate_passport_extension],
    )
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['job', 'email'], name='unique_application_job_email'),
        ]

    def __str__(self):
        return f"{self.first_name} {self.surname} - {self.job.job_title}"


class Employee(models.Model):
    """Additional onboarding details captured when an approved applicant is added as an employee."""
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='employee')
    share_code = models.CharField(max_length=20, blank=True)
    educational_qualification = models.CharField(max_length=255, blank=True)
    cv = models.FileField(
        upload_to='employees/cv/',
        validators=[validate_document_size, validate_document_extension],
        blank=True, null=True,
    )
    passport_number = models.CharField(max_length=20, blank=True)
    passport_photo = models.FileField(
        upload_to='employees/passport_photos/',
        verbose_name='Passport size photo',
        validators=[validate_document_size, validate_photo_extension],
        blank=True, null=True,
    )
    dbs_certificate = models.FileField(
        upload_to='employees/dbs/',
        verbose_name='DBS certificate',
        validators=[validate_document_size, validate_document_extension],
        blank=True, null=True,
    )
    pcc_certificate = models.FileField(
        upload_to='employees/pcc/',
        verbose_name='PCC certificate',
        validators=[validate_document_size, validate_document_extension],
        blank=True, null=True,
    )
    right_to_work = models.FileField(
        upload_to='employees/right_to_work/',
        verbose_name='Right to work',
        validators=[validate_document_size, validate_document_extension],
        blank=True, null=True,
    )
    extra_documents = models.FileField(
        upload_to='employees/extra_documents/',
        verbose_name='Extra documents',
        validators=[validate_document_size, validate_document_extension],
        blank=True, null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Employee: {self.application.first_name} {self.application.surname}"
