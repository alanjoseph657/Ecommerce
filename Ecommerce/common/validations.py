import re

from django.contrib.auth.models import User
from django.core.validators import EmailValidator

from decimal import Decimal, InvalidOperation



def validate_alphanumeric_with_spaces(input_string):    
    if not isinstance(input_string, str):
        return False
    
    pattern = re.compile(r'^[a-zA-Z0-9\s]+$')
    
    if not pattern.match(input_string):
        return False
    
    return True


def validate_product_name(input_string):
    if not isinstance(input_string, str):
        return False
    
    pattern = re.compile(r'^[a-zA-Z0-9\s.,]+$')
    
    if not pattern.match(input_string):
        return False
    
    return True


def validate_price(price):
    if not isinstance(price, (int, float, Decimal, str)):
        return False

    try:
        price = Decimal(price)
    except (InvalidOperation, ValueError):
        return False

    if price < 0:
        return False

    if price.as_tuple().exponent < -2:
        return False

    return True


def validate_image(file):
    image_mime_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    return file.content_type in image_mime_types


def validate_video(file):
    video_mime_types = ['video/mp4', 'video/webm', 'video/ogg']
    return file.content_type in video_mime_types


def validate_username(input_string):
    if not isinstance(input_string, str):
        return "Invalid Input"
    
    if not (5 <= len(input_string) <= 30):
        return "Username must be between 5 and 30 characters."

    pattern = re.compile(r'^[a-zA-Z0-9_]+$')
    
    if not pattern.match(input_string):
        return "Username can only contain alphanumeric characters and hyphens."
    
    if re.match(r'^[_-]|[_-]$', input_string):
        return "Username should not start or end with underscores or hyphens."
    
    if User.objects.filter(username=input_string).exists():
        return "Username is already taken."
    
    return True


def validate_email(input_email):
    if not EmailValidator(input_email):
        return False
    
    if User.objects.filter(email=input_email).exists():
        return False
    
    return True


def validate_message_email(input_email):
    if not EmailValidator(input_email):
        return False
    
    return True


def validate_password(input_string):
    if len(input_string) < 8:
        return "Password must be at least 8 characters long."
    
    if not re.search(r'[A-Z]', input_string):
        return "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', input_string):
        return "Password must contain at least one lowercase letter."
    if not re.search(r'[0-9]', input_string): 
        return "Password must contain at least one digit."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', input_string): 
        return "Password must contain at least one special character."
    

    common_patterns = ['password', '123456', 'qwerty', 'letmein']
    if any(pattern in input_string.lower() for pattern in common_patterns):
        return "Password contains a common pattern."

    return True