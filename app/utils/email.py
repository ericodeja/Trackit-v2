from fastapi import BackgroundTasks
import smtplib
from email.mime.text import MIMEText
from app.core.config import settings
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = settings.SMTP_USER
SMTP_PASS = settings.SMTP_PASS


def password_reset_email(background_tasks: BackgroundTasks, email: str, reset_link: str):

    subject = 'Password Reset Link'
    body = f'Click this link to reset your password: {reset_link}'
    msg = MIMEText(body, 'plain')
    msg['Subject'] = subject
    if not SMTP_USER:
        raise ValueError('Missing SMTP_USER')
    msg['FROM'] = SMTP_USER
    msg['TO'] = email

    def send_mail():
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                if not SMTP_USER:
                    raise ValueError('Missing SMTP_USER')
                if not SMTP_PASS:
                    raise ValueError('Missing SMTP_PASS')
                server.login(SMTP_USER, SMTP_PASS)
                server.sendmail(SMTP_USER, email, msg.as_string())
                logger.info(f'Password reset email sent to {email}')
        except Exception as e:
            logger.info(f'Failed to send email to {email}')
            

    background_tasks.add_task(send_mail)
