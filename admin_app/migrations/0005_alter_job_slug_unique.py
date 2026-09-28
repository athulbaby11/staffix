# Now that every existing row has a populated slug, enforce uniqueness and
# drop nullability so it behaves like a normal required field going forward
# (new rows always get one generated in Job.save()).

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0004_populate_job_slugs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='slug',
            field=models.SlugField(blank=True, max_length=280, unique=True),
        ),
    ]
