from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def reset_password_token_created(sender, instance, reset_password_token, *args,  **kwargs):
    context = {
        'current_user' : reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    }
    email_html_message = render_to_string('email/reset_password.html', context)
    email_plaintex_message = render_to_string('email/reset_password.txt', context)

    msg = EmailMultiAlternatives(
        "password Reset for {title}".format(title="jobConnect password reset link"),
       email_plaintex_message,
       "nonreply@jobconnect.com",
       [reset_password_token.user.email]
    )

    msg.attach_alternative(email_html_message, "text/html")
    msg.send()