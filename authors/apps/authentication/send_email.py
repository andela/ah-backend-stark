import os
import ssl
import sendgrid
from sendgrid.helpers.mail import Mail, Email, Content

ssl._create_default_https_context = ssl._create_unverified_context


def send_mail(recipient, subject, content):
    """"This method handles emails sent to a user"""

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email('authors.haven.stark@gmail.com')
    to_email = Email(recipient)
    content = Content("text/plain", content)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return (response.status_code)
