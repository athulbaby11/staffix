import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'staffix.settings')
django.setup()

from django.contrib.auth.models import User

email = os.environ.get('STAFFIX_ADMIN_EMAIL')
password = os.environ.get('STAFFIX_ADMIN_PASSWORD')
username = os.environ.get('STAFFIX_ADMIN_USERNAME', 'admin')
if not email or not password:
    raise SystemExit("Set STAFFIX_ADMIN_EMAIL and STAFFIX_ADMIN_PASSWORD before running this script.")

user, created = User.objects.get_or_create(username=username, defaults={'email': email})
user.email = email
user.set_password(password)
user.is_staff = True
user.is_superuser = True
user.save()

print('created' if created else 'updated', user.username, user.email)
