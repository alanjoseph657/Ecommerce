import random

from django.core.mail import send_mail

from Ecommerce import settings


def generate_otp():
    return str(random.randint(1000, 9999))


def send_otp_email(email, otp):
    subject = 'Your OTP for Password Reset'
    message = f'Your OTP for password reset is: {otp}'
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [email])


def send_otp_email_verification(email, otp):
    subject = 'Your OTP for Email Verification'
    message = f'Your OTP for Email Verification is: {otp}'
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [email])


def order_confirmation_mail(email, order_id):
    subject = f'Order Placed #{order_id}'
    message = f'Your order #{order_id} has been confirmed.'
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [email])