import asyncio
import smtplib
from django.conf.global_settings import EMAIL_HOST
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from gofresh.settings import get_running_host, SENDGRID_API_KEY, SENDGRID_SENDER


#loop = asyncio.get_event_loop()

async def send_account_verification_email(name, email, email_confirmation_key):
    try:

        email_confirmation_url = get_running_host() + "/confirm_email/" + email_confirmation_key
        html_content = render_to_string('accounts/signup_email.html', {'name': name,
                                                                       'email_confirmation_url': email_confirmation_url})
        subject, from_email, to = 'Welcome to GoFresh', EMAIL_HOST, email
        send_mail(subject=subject, message=html_content, from_email=from_email, recipient_list={to}, fail_silently=False, html_message=html_content)

        return True

    except smtplib.SMTPException:
        return False


def got_result(future):
    print(future.result())


def async_verification_email(name, email, email_confirmation_key):
    loop = asyncio.new_event_loop()
    task = loop.create_task(send_account_verification_email(name, email, email_confirmation_key))
    task.add_done_callback(got_result)
    loop.run_until_complete(task)