from django import forms
from ..models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
             attrs={
                'class': 'registration-input',
                'placeholder': 'you@example.com',
                'autofocus': True,
                'autocomplete': 'email',
                'name': 'email'
            }
        )
    )
    
    password1 = forms.CharField(
            widget=forms.PasswordInput(
                attrs={
                    'class': 'registration-input',
                    'placeholder': 'Введи пароль',
                    'autocomplete': 'current-password',
                    'name': 'password1',
                    'id': 'password1'
                }
            )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'registration-input',
                'placeholder': 'Введи пароль',
                'name': 'password2',
                'id': 'password2'
            }
        )
    )


    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Паролі не співпадають')

        return password2
    

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Користувач з таким email вже існує')
        
        return email
