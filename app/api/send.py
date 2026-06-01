from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
from app.services import mailer
from app.core.config import settings

router = APIRouter(prefix="/send", tags=["Send"])


def _require_api_key(x_api_key: str = Header(..., alias="X-Api-Key")):
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


class VerificationPayload(BaseModel):
    to_email: EmailStr
    username: str
    token: str


class PasswordResetPayload(BaseModel):
    to_email: EmailStr
    username: str
    token: str


class AnnouncementPayload(BaseModel):
    to_emails: List[EmailStr]
    subject: str
    body: str


@router.post("/verification", dependencies=[Depends(_require_api_key)])
def send_verification(payload: VerificationPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        mailer.send_verification_email,
        payload.to_email, payload.username, payload.token,
    )
    return {"queued": True}


@router.post("/password-reset", dependencies=[Depends(_require_api_key)])
def send_password_reset(payload: PasswordResetPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        mailer.send_password_reset_email,
        payload.to_email, payload.username, payload.token,
    )
    return {"queued": True}


@router.post("/announcement", dependencies=[Depends(_require_api_key)])
def send_announcement(payload: AnnouncementPayload, background_tasks: BackgroundTasks):
    for email in payload.to_emails:
        background_tasks.add_task(
            mailer.send_announcement_email,
            email, payload.subject, payload.body,
        )
    return {"queued": True, "recipients": len(payload.to_emails)}
