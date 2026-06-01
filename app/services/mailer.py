import smtplib
import ssl
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

logger = logging.getLogger(__name__)


def _send(to_email: str, subject: str, html: str) -> None:
    """Core SMTP send. Runs inside BackgroundTasks (thread pool — non-blocking)."""
    if not settings.SMTP_ENABLED:
        logger.info(f"[SMTP disabled] To={to_email} | Subject={subject}")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_USERNAME}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html, "html"))

    ctx = ssl.create_default_context()
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.ehlo()
        server.starttls(context=ctx)
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USERNAME, to_email, msg.as_string())

    logger.info(f"[SMTP] Sent → {to_email}: {subject}")


def send_verification_email(to_email: str, username: str, token: str) -> None:
    verify_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    html = f"""<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;background:#f4f4f4;padding:20px;margin:0;">
  <div style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:10px;padding:36px;">
    <h2 style="color:#4F46E5;margin:0 0 8px;">Verify your email</h2>
    <p style="color:#374151;">Hi <strong>{username}</strong>,</p>
    <p style="color:#374151;">Thanks for signing up for <strong>Netra</strong>. Click the button below to verify your email address and activate your account.</p>
    <a href="{verify_url}"
       style="display:inline-block;margin:20px 0;padding:12px 28px;background:#4F46E5;color:#ffffff;text-decoration:none;border-radius:7px;font-weight:bold;font-size:15px;">
      Verify Email
    </a>
    <p style="color:#6B7280;font-size:13px;">This link expires in <strong>24 hours</strong>. If you didn't create a Netra account, you can safely ignore this email.</p>
    <hr style="border:none;border-top:1px solid #E5E7EB;margin:24px 0;">
    <p style="color:#9CA3AF;font-size:12px;margin:0;">Netra &middot; Personal Knowledge Chatbot</p>
  </div>
</body>
</html>"""
    _send(to_email, "Verify your Netra account", html)


def send_password_reset_email(to_email: str, username: str, token: str) -> None:
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    html = f"""<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;background:#f4f4f4;padding:20px;margin:0;">
  <div style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:10px;padding:36px;">
    <h2 style="color:#4F46E5;margin:0 0 8px;">Reset your password</h2>
    <p style="color:#374151;">Hi <strong>{username}</strong>,</p>
    <p style="color:#374151;">We received a request to reset your <strong>Netra</strong> password. Click the button below to set a new one.</p>
    <a href="{reset_url}"
       style="display:inline-block;margin:20px 0;padding:12px 28px;background:#4F46E5;color:#ffffff;text-decoration:none;border-radius:7px;font-weight:bold;font-size:15px;">
      Reset Password
    </a>
    <p style="color:#6B7280;font-size:13px;">This link expires in <strong>1 hour</strong>. If you didn't request a password reset, you can safely ignore this email.</p>
    <hr style="border:none;border-top:1px solid #E5E7EB;margin:24px 0;">
    <p style="color:#9CA3AF;font-size:12px;margin:0;">Netra &middot; Personal Knowledge Chatbot</p>
  </div>
</body>
</html>"""
    _send(to_email, "Reset your Netra password", html)


def send_announcement_email(to_email: str, subject: str, body: str) -> None:
    html = f"""<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;background:#f4f4f4;padding:20px;margin:0;">
  <div style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:10px;padding:36px;">
    <h2 style="color:#4F46E5;margin:0 0 16px;">{subject}</h2>
    <div style="color:#374151;line-height:1.7;">{body}</div>
    <hr style="border:none;border-top:1px solid #E5E7EB;margin:24px 0;">
    <p style="color:#9CA3AF;font-size:12px;margin:0;">
      Netra &middot; <a href="{settings.FRONTEND_URL}" style="color:#4F46E5;text-decoration:none;">Visit app</a>
    </p>
  </div>
</body>
</html>"""
    _send(to_email, subject, html)
