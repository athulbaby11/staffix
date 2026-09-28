import os
import re
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "staffix.settings")
django.setup()

from django.test import Client

email = os.environ.get("STAFFIX_ADMIN_EMAIL")
password = os.environ.get("STAFFIX_ADMIN_PASSWORD")
if not email or not password:
    raise SystemExit("Set STAFFIX_ADMIN_EMAIL and STAFFIX_ADMIN_PASSWORD before running this script.")

c = Client()
r = c.get("/login")
m = re.search(r"name=\"csrfmiddlewaretoken\" value=\"([^\"]+)\"", r.content.decode())
token = m.group(1)
r2 = c.post("/login", {"csrfmiddlewaretoken": token, "email": email, "password": password})
print(r2.status_code)
print(r2.content.decode()[:4000])
