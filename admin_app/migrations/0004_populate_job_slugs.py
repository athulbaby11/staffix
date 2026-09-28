import secrets

from django.db import migrations
from django.template.defaultfilters import slugify


def populate_slugs(apps, schema_editor):
    Job = apps.get_model('admin_app', 'Job')
    existing_slugs = set()
    for job in Job.objects.all():
        base_slug = slugify(job.job_title) or 'job'
        while True:
            candidate = f"{base_slug}-{secrets.token_hex(4)}"
            if candidate not in existing_slugs:
                break
        existing_slugs.add(candidate)
        job.slug = candidate
        job.save(update_fields=['slug'])


def reverse_noop(apps, schema_editor):
    # Slugs are simply cleared back to null; no data loss for other fields.
    Job = apps.get_model('admin_app', 'Job')
    Job.objects.update(slug=None)


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0003_job_slug'),
    ]

    operations = [
        migrations.RunPython(populate_slugs, reverse_noop),
    ]
