# STAFFIX API

The versioned REST API is intended for mobile clients such as a future Flutter app. Existing website routes and behavior are unchanged.

## Public job endpoints

- `GET /api/v1/jobs/` returns the available jobs in pages of 20. Use `?page=2` for subsequent pages.
- `GET /api/v1/jobs/{slug}/` returns one job.

Job responses include the slug, company, title, description, location, salary, job type, and employment type.
The list response includes `count`, `next`, `previous`, and `results` fields.

## Authentication

Use the existing Django account credentials to request an API token:

```http
POST /api/v1/auth/token/
Content-Type: application/json

{"username": "your-username", "password": "your-password"}
```

The response contains a token:

```json
{"token": "your-token"}
```

Send it on authenticated requests as `Authorization: Token your-token`. To verify the token and retrieve the signed-in username, use `GET /api/v1/auth/me/`.

Token-authenticated requests must use HTTPS in production. Tokens are long-lived credentials; keep them private and revoke them if a device is lost or access should be removed.
