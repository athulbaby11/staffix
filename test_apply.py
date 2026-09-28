import requests

s = requests.Session()
r = s.get("http://127.0.0.1:8000/apply/29/")
csrftoken = s.cookies.get("csrftoken")

files = {"passport": ("test.png", b"\x89PNG\r\n\x1a\n" + b"0"*50, "image/png")}
data = {
    "first_name": "",
    "surname": "",
    "email": "not-an-email",
    "phone_number": "123",
    "ni_number": "bad",
    "address": "",
    "dob": "",
    "captcha": "0",
    "csrfmiddlewaretoken": csrftoken,
}
r2 = s.post("http://127.0.0.1:8000/apply/29/", data=data, files=files, headers={"X-Requested-With": "XMLHttpRequest", "Referer": "http://127.0.0.1:8000/apply/29/"})
print(r2.status_code)
print(r2.json())
