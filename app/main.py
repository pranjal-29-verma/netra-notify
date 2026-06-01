from fastapi import FastAPI
from app.core.config import settings
from app.api.send import router as send_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Internal email/notification service for Netra. "
                "Requires X-Api-Key header matching the configured API_KEY.",
)

app.include_router(send_router)


@app.get("/health")
def health():
    return {"status": "healthy", "smtp_enabled": settings.SMTP_ENABLED}
