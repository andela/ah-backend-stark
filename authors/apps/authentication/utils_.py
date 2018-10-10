import os
import ssl
import sendgrid
from sendgrid.helpers.mail import *

ssl._create_default_https_context = ssl._create_unverified_context


def sendMail(recipient, title, body):
    """
    This is a method for implementing the send email fuctionality
  """
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("authors.haven.stark@gmail.com")
    to_email = Email(recipient)
    subject = title
    content = Content("text/plain", body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return response.status_code