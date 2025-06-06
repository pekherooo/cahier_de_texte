from flask_mail import Message
from app.extensions import mail
from flask import current_app

def send_email(subject, recipients, body):
    msg = Message(subject=subject, recipients=recipients, body=body)
    try:
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Erreur lors de l'envoi du mail: {e}")
        return False
