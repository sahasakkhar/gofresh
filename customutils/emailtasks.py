import asyncio
import smtplib
from django.conf.global_settings import EMAIL_HOST
from django.core.mail import EmailMessage, send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from gofresh.settings import get_running_host, SENDGRID_API_KEY, SENDGRID_SENDER
import _thread, threading

#loop = asyncio.get_event_loop()


class SendAccountVerificationEmail(threading.Thread):

    def __init__(self, name, email, email_confirmation_key):
        threading.Thread.__init__(self)

        self.name = name
        self.email = email
        self.email_confirmation_key = email_confirmation_key

    def run(self):
        try:

            email_confirmation_url = get_running_host() + "/confirm_email/" + self.email_confirmation_key
            html_content = render_to_string('accounts/signup_email.html', {'name': self.name, 'email_confirmation_url': email_confirmation_url})
            subject = 'Welcome to GoFresh'
            send_mail(subject, html_content, SENDGRID_SENDER, [self.email], fail_silently=False, html_message=html_content)

            '''
            mail = EmailMultiAlternatives(
                subject=subject,
                body=html_content,
                from_email=SENDGRID_SENDER,
                to=[self.email],
            )
            mail.send()
            '''

            print('SendAccountVerificationEmail sent')

        except smtplib.SMTPException:
            print('SendAccountVerificationEmail failed')


class ForgotPasswordEmail(threading.Thread):

    def __init__(self, name, email, password_reset_link):
        threading.Thread.__init__(self)

        self.name = name
        self.email = email
        self.password_reset_link = password_reset_link

    def run(self):
        try:
            subject, from_email, to = 'You have been requested for password reset email.!', EMAIL_HOST, self.email
            html_content = render_to_string('accounts/forgot_password_reset_email.html', {'name': self.name,
                                                                                          'password_reset_link': self.password_reset_link})
            send_mail(subject, html_content, SENDGRID_SENDER, [self.email],
                      fail_silently=False, html_message=html_content)
            print('ForgotPasswordEmail sent')

        except smtplib.SMTPException:
            print('ForgotPasswordEmail failed')