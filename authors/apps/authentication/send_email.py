import os
from django.core.mail import send_mail


def send_email(recipient, subject, message):
    """"
    This method sends emails to a given user
    """
    from_email = os.getenv("EMAIL_SENDER")
    status = send_mail(subject, message, from_email, [recipient])
    return status
