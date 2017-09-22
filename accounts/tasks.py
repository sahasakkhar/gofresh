import os
import smtplib

from django.conf.global_settings import EMAIL_HOST
from sendgrid import *
from sendgrid.helpers.mail import *
from celery.exceptions import MaxRetriesExceededError
from django.core.mail import EmailMessage, send_mail

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from gofresh.celery import app
from gofresh.settings import get_running_host, SENDGRID_API_KEY, SENDGRID_SENDER



@app.task(bind=True, ignore_result=True, max_retries=3, default_retry_delay=3)
def account_confirmation_email(self, name, email, email_confirmation_key):

    try:

        email_confirmation_url = get_running_host() + "/confirm_email/" + email_confirmation_key
        html_content = render_to_string('accounts/signup_email.html', {'name': name,
                                                                       'email_confirmation_url': email_confirmation_url})
        subject, from_email, to = 'Welcome to GoFresh', EMAIL_HOST, email
        send_mail(subject=subject, message=html_content, from_email=from_email, recipient_list={to}, fail_silently=False, html_message=html_content)

        return True

    except smtplib.SMTPException:
        return False


'''

@app.task(bind=True, ignore_result=True, max_retries=3, default_retry_delay=3)
def account_confirmation_email(self, name, email, email_confirmation_key):

    print('%s %s %s' % (name, email, email_confirmation_key))
    try:

        email_confirmation_url = get_running_host() + "/confirm_email/" + email_confirmation_key
        html_content = render_to_string('accounts/signup_email.html', {'name': name,
                                                                       'email_confirmation_url': email_confirmation_url})
        #subject, from_email, to = 'Welcome to GoFresh', EMAIL_HOST, email
        #send_mail(subject=subject, message=html_content, from_email=from_email, recipient_list={email}, fail_silently=False, html_message=html_content)

        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        subject = 'Welcome to GoFresh'
        from_email = Email(SENDGRID_SENDER)
        to_email = Email(email)

        content = Content("text/html", html_content)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())

        print(response.status_code)
        print(response.body)
        print(response.headers)


        return True

    except smtplib.SMTPException:
        return False
'''

'''
@app.task(bind=True, ignore_result=True, max_retries=3, default_retry_delay=3)
def account_confirmation_email(self, name, email, email_confirmation_key):

    try:

        email_confirmation_url = get_running_host() + "/confirm_email/" + email_confirmation_key
        html_content = render_to_string('accounts/signup_email.html', {'name': name,
                                                                       'email_confirmation_url': email_confirmation_url})
        #subject, from_email, to = 'Welcome to GoFresh', EMAIL_HOST, email
        #send_mail(subject=subject, message=html_content, from_email=from_email, recipient_list={email}, fail_silently=False, html_message=html_content)

        sg = SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        subject = 'Welcome to GoFresh'
        from_email = Email(SENDGRID_SENDER, 'GoFresh')
        to_email = Email(email, name)

        mail = Mail()

        mail.set_from(from_email)

        mail.set_subject(subject)

        personalization = Personalization()
        personalization.add_to(to_email)
        mail.add_personalization(personalization)

        mail.add_content(Content("text/html", html_content))

        mail_settings = MailSettings()
        mail_settings.set_sandbox_mode(SandBoxMode(False))
        mail.set_mail_settings(mail_settings)

        data = mail.get()
        response = sg.client.mail.send.post(request_body=data)

        print(response.status_code)
        print(response.headers)
        print(response.body)

        return True

    except smtplib.SMTPException:
        return False

'''


@app.task(bind=True, ignore_result=True, max_retries=3, default_retry_delay=3)
def forgot_password_email_send(self, name, email, password_reset_link):

    try:
        subject, from_email, to = 'You have been requested for password reset email.!', EMAIL_HOST, email
        html_content = render_to_string('accounts/forgot_password_reset_email.html', {'name': name,
                                                                       'password_reset_link': password_reset_link})
        send_mail(subject=subject, message=html_content, from_email=from_email, recipient_list={email},
                      fail_silently=False, html_message=html_content)
        return True

    except smtplib.SMTPException:
        return False
