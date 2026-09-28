import os
import re
import io
import requests

BASE = "http://127.0.0.1:8000"
email = os.environ.get("STAFFIX_ADMIN_EMAIL")
password = os.environ.get("STAFFIX_ADMIN_PASSWORD")
if not email or not password:
    raise SystemExit("Set STAFFIX_ADMIN_EMAIL and STAFFIX_ADMIN_PASSWORD before running this script.")

s = requests.Session()

def get_csrf(html):
    m = re.search(r"name=[\"']csrfmiddlewaretoken[\"'] value=[\"']([^\"']+)[\"']", html)
    return m.group(1) if m else None

# 1. Login
r = s.get(BASE + "/login")
token = get_csrf(r.text)
r = s.post(BASE + "/login", data={
    "csrfmiddlewaretoken": token,
    "email": email,
    "password": password,
}, allow_redirects=True)
print("login status:", r.status_code, "final url:", r.url)
assert "admin_dashboard" in r.url or "dashboard" in r.url, "login did not redirect to dashboard"

# 2. Onboard page - find an approved application id with "Add as our employee" link
r = s.get(BASE + "/onboard")
print("onboard status:", r.status_code)
m = re.search(r"/add_employee/(\d+)", r.text)
assert m, "No add_employee link found on onboard page -- no approved applications?"
app_id = m.group(1)
print("Found application id:", app_id)
assert "Add as our employee" in r.text
print("onboard page contains 'Add as our employee' button: OK")

# 3. Get add_employee page
r = s.get(BASE + f"/add_employee/{app_id}")
print("add_employee GET status:", r.status_code)
assert r.status_code == 200
token2 = get_csrf(r.text)
assert token2

# 4. Submit employee details with files
def make_file(name, content=b"%PDF-1.4 test content"):
    return (name, io.BytesIO(content), "application/pdf")

files = {
    "cv": make_file("cv.pdf"),
    "passport_photo": ("photo.png", io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"0"*50), "image/png"),
    "dbs_certificate": make_file("dbs.pdf"),
    "pcc_certificate": make_file("pcc.pdf"),
}
data = {
    "csrfmiddlewaretoken": token2,
    "share_code": "AB123456CD",
    "educational_qualification": "BSc Nursing",
    "passport_number": "P1234567",
}
r = s.post(BASE + f"/add_employee/{app_id}", data=data, files=files, headers={"X-Requested-With": "XMLHttpRequest"})
print("add_employee POST status:", r.status_code)
print("response:", r.text[:500])
assert r.status_code == 200
assert r.json().get("success") is True, r.json()
print("Employee details saved successfully!")

# 5. Reload onboard page -> should now show "Edit employee details"
r = s.get(BASE + "/onboard")
assert f"/add_employee/{app_id}" in r.text
assert "Edit employee details" in r.text
print("onboard page now shows 'Edit employee details': OK")

print("\nALL EMPLOYEE FLOW TESTS PASSED")
