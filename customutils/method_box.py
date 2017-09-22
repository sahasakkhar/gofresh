import hmac
import random
import string
import uuid
import hashlib

from django.core.cache import cache

from accounts.models import PasswordResetKey, EmailConfirmationKey
from django.core.exceptions import ValidationError
from django.forms import EmailField

from gofresh.settings import DEBUG, get_running_host


def get_confirmation_email_subject_message(user):
    email_confirmation_key = create_email_confirm_key(user)
    subject = 'Welcome to GoFresh'
    confirmation_link = get_running_host() + "confirm_email/" + email_confirmation_key + "/"
    message = """<html><body><h4>Click the link below to activate your account!</h4><br><br>
        <a href="mylink">Click here</a>
        </body>
        </html>\
        """
    message = message.replace('mylink', confirmation_link)
    return subject, message


def get_forget_password_email_subject_message(user):
    password_reset_key = create_password_reset_key(user)
    subject = 'You have been requested for password reset email.!'
    password_reset_link = get_running_host() + "forgot_password_form/" + password_reset_key + "/"
    message = """<html><body><h4>Click the button below to reset your password!</h4><br><br>
        <a href="mylink">Click here</a>
        </body>
        </html>\
        """
    message = message.replace('mylink', password_reset_link)
    return subject, message


def create_email_confirm_key(user):
    key = generate_key()
    if not EmailConfirmationKey.objects.filter(key=key).exists():
        EmailConfirmationKey.objects.create(auth_user=user, key=key)
        return key
    else:
        create_email_confirm_key(user)


def create_password_reset_key(user):
    key = generate_key()
    if not PasswordResetKey.objects.filter(key=key).exists():
        PasswordResetKey.objects.create(auth_user=user, key=key)
        return key
    else:
        create_password_reset_key(user)


def generate_key():
    new_uuid = uuid.uuid4()
    key = hmac.new(new_uuid.bytes, digestmod=hashlib.sha1).hexdigest()
    return key


def generate_invoice_number():
    from orders.models import Order
    invoice_no = id_generator()
    try :
        Order.objects.get(invoice_number=invoice_no)
        generate_invoice_number()
    except Order.DoesNotExist:
        return  invoice_no


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_delivery_cost():

    '''
    fo = open('delivery_cost.txt', 'r')
    delivery_cost = int(fo.read())
    fo.close()

    '''

    return int(cache.get('delivery_cost', 30))
