# Staffix – Deployment Notes (for DevOps)

Django 6.1 app (Python 3.13), WSGI entry: `staffix.wsgi:application`.

## Steps
1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` (or set real env vars). With `DJANGO_DEBUG=false`
   the app refuses to start without `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS`.
   Also set `DJANGO_CSRF_TRUSTED_ORIGINS=https://<domain>`.
3. `python manage.py migrate`
4. `python manage.py collectstatic --noinput` (static files are served by WhiteNoise)
5. Run: `gunicorn staffix.wsgi:application --bind 0.0.0.0:8000 --workers 3`
6. Put it behind a TLS-terminating reverse proxy that sends `X-Forwarded-Proto: https`.
7. Create an admin user: `STAFFIX_ADMIN_PASSWORD=... python create_admin.py`

## Important
- **Uploaded media (`/media/`) contains private documents** (CVs, DBS, passports, right-to-work).
  Django only serves `/media/` automatically in DEBUG. Do NOT expose the whole media
  directory publicly; serve it only to authenticated users (e.g. nginx `internal` + `X-Accel-Redirect`)
  or move to private object storage.
- Database is SQLite by default. Keep `DJANGO_DB_PATH` and `DJANGO_MEDIA_ROOT` on persistent
  storage (not ephemeral container disk), or switch `DATABASES` to PostgreSQL.
- Backups: `python manage.py backup_db` (see `scripts/linux` for systemd timer / cron).
- Email uses the console backend until `DJANGO_EMAIL_*` is configured.
- Debug/test scripts in the repo root (`debug_login*.py`, `test_*.py`) are for local use only.

## Render
1. Push to GitHub, then in Render choose New > Blueprint and select this repo (uses `render.yaml`).
2. Fill in `DJANGO_ALLOWED_HOSTS` (e.g. `staffix.onrender.com`) and `DJANGO_CSRF_TRUSTED_ORIGINS` (`https://staffix.onrender.com`).
3. After the first deploy, open the Render Shell and run `STAFFIX_ADMIN_PASSWORD=... python create_admin.py`.
- Free plan, no persistent disk: the SQLite DB and uploaded media are wiped on every deploy/restart
  (and the service sleeps after idle), so the admin user must be recreated. Demo/testing only.
