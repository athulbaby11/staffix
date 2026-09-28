import re
import os
import requests

email = os.environ.get("STAFFIX_ADMIN_EMAIL")
password = os.environ.get("STAFFIX_ADMIN_PASSWORD")
if not email or not password:
    raise SystemExit("Set STAFFIX_ADMIN_EMAIL and STAFFIX_ADMIN_PASSWORD before running this script.")

r = requests.get("http://127.0.0.1:8000/login/")
print("status:", r.status_code)
m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', r.text)
print("token:", m.group(1) if m else None)

if m:
    token = m.group(1)
    r2 = requests.post(
        "http://127.0.0.1:8000/login/",
        data={"csrfmiddlewaretoken": token, "email": email, "password": password},
        cookies=r.cookies,
    )
    print("login status:", r2.status_code)
    print(r2.text[:5000])
