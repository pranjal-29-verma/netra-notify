# netra-notify

Internal email/notification microservice for Netra. Handles all outbound emails (verification, password reset, announcements) via Gmail SMTP. Secured with a shared API key — only `netra-app` should call it.

---

## Prerequisites

- Python 3.10+
- A Gmail account with **2-Step Verification** enabled
- A Gmail **App Password** (not your regular Gmail password)

### Generate a Gmail App Password

1. Go to [Google Account](https://myaccount.google.com) → **Security**
2. Under "How you sign in to Google", open **2-Step Verification**
3. Scroll to the bottom → **App passwords**
4. Select app: **Mail**, device: **Other** → enter "Netra Notify"
5. Copy the 16-character password — use it as `SMTP_PASSWORD` below

---

## Local Setup

### 1. Clone and enter the directory

```bash
git clone https://github.com/pranjal-29-verma/netra-notify.git
cd netra-notify
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
SMTP_USERNAME=your@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SMTP_ENABLED=true

FRONTEND_URL=http://localhost:5173

# Must match NOTIFY_API_KEY in netra-app's .env
API_KEY=change-me-in-production
```

> Set `SMTP_ENABLED=false` to disable actual sending — emails will be logged to the console instead (useful for development without Gmail configured).

### 5. Run the service

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Service is now running at **http://localhost:8001**

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check + SMTP status |
| `POST` | `/send/verification` | Send email verification link |
| `POST` | `/send/password-reset` | Send password reset link |
| `POST` | `/send/announcement` | Send bulk announcement email |

All `/send/*` endpoints require the header:
```
X-Api-Key: <your API_KEY>
```

### Example — test verification email via curl

```bash
curl -X POST http://localhost:8001/send/verification \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: change-me-in-production" \
  -d '{"to_email": "test@example.com", "username": "testuser", "token": "abc123"}'
```

---

## Connecting with netra-app

Add these to `netra-app/.env`:

```env
NOTIFY_BASE_URL=http://localhost:8001
NOTIFY_API_KEY=change-me-in-production   # must match API_KEY above
NOTIFY_ENABLED=true
```

---

## API Docs

FastAPI auto-generates interactive docs when running locally:

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc
