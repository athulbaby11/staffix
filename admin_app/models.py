import secrets

from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Job(models.Model):
    company_name = models.CharField(max_length=255, default='')
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50, choices=[('full_time', 'Full Time'), ('part_time', 'Part Time')])
    employment_type = models.CharField(max_length=50, choices=[('permanent', 'Permanent'), ('temporary', 'Temporary')])
    # Unique, hard-to-guess URL segment (e.g. "care-worker-a1b2c3d4") used for
    # the public job link/apply link, so sharing a job's URL can't be used to
    # discover or apply to other jobs by guessing sequential IDs.
    slug = models.SlugField(max_length=280, unique=True, blank=True)

    def __str__(self):
        return self.job_title

    def _generate_unique_slug(self):
        base_slug = slugify(self.job_title) or 'job'
        while True:
            candidate = f"{base_slug}-{secrets.token_hex(4)}"
            if not Job.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                return candidate

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)
