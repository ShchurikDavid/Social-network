import random
from django.http import HttpRequest
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password

from ..models import User
from ..services.email_service import send_email_code

def generate_code(length=6):
    code = ''
    list_numbers = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'

    for numb in range(length):
        code += random.choice(list_numbers)

    return code

def save_registration(request: HttpRequest, cleaned_data):
    try:
        code = generate_code()
        # request.session['registration_data'] = cleaned_data
        
        request.session['registration_data'] = {
            'email': cleaned_data['email'],
            'password': make_password(cleaned_data['password1'])
        }
        request.session['confirm_code'] = code

        send_email_code(cleaned_data['email'], code)
        
    except IntegrityError:
        return {
            'error': 'Користувач з таким email вже існує'
        }

def confirm_email(request: HttpRequest, cleaned_data):
    if request.session.get('confirm_code') != cleaned_data['confirm_code'].strip():  
        return None
                  
    user_data = request.session.get('registration_data')

    user = User.objects.create(
        email = user_data['email'].strip(),
        password = user_data['password']
    )

    return user

