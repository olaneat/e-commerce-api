from django.core.mail import EmailMessage
from django.conf import settings

class Utils:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(
            from_email=settings.DEFAULT_FROM_EMAIL,
            subject=data['subject'], body=data['body'], to=[
                data['recipient']]
        )
        email.send()
