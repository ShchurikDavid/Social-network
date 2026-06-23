import bcrypt

from django import forms
from django.contrib.auth import authenticate
from ..models import User


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
             attrs = {
                'class': 'registration-input',
                'placeholder': 'you@example.com',
                'autofocus': True,
                'autocomplete': 'email',
                'name': 'email'
            }
        )
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs = {
                'class': 'registration-input',
                'placeholder': 'Введи пароль',
                'autocomplete': 'current-password',
                'name': 'password',
                'id': 'password3'
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        
        email = cleaned_data.get('email').strip()
        password = cleaned_data.get('password')
        user = User.objects.filter(email=email).first()

        if not user:
            return False
        
        password_bytes = password.encode('utf-8')
        hash_bytes = user.password

        # print('password_bytes',password_bytes, hash_bytes, bcrypt.checkpw(password_bytes, hash_bytes))
        self.user = None
        if hash_bytes.startswith("$2"):
            try:
                if bcrypt.checkpw(password_bytes, hash_bytes.encode('utf-8')):
                    self.user = user
            except ValueError:
                pass
        
        if self.user is None:
            user = authenticate(email=email, password=password)

            if not user:
                raise forms.ValidationError("Неверный email или пароль")
            
            self.user = user

        if self.user is None:
            return False

        return cleaned_data
