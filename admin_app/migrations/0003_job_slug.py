# Generated manually (split into steps so existing rows can be safely
# backfilled with a unique slug before the unique constraint is enforced).

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0002_job_company_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='slug',
            field=models.SlugField(blank=True, max_length=280, null=True, unique=False),
        ),
    ]
