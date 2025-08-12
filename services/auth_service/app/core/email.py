import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..core.config import get_settings


def send_email(to: str, subject: str, body: str):
    cfg = get_settings()
    if not (cfg.smtp_host and cfg.smtp_port and cfg.smtp_user and cfg.smtp_pass):
        return

    message = MIMEMultipart()
    message["From"] = cfg.smtp_user
    message["To"] = to
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(cfg.smtp_host, cfg.smtp_port) as server:
        server.login(cfg.smtp_user, cfg.smtp_pass)
        server.sendmail(cfg.smtp_user, to, message.as_string())
