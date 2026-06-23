import re
from django import forms

from user_app.models import User
from profile_app.models import Profile  


class ProfileForm(forms.Form):
    username = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(
            attrs={
                'class': 'registration-input',
                'placeholder': 'Введіть Псевдонім автора',
                'autofocus': True,
                'name': 'username'
                
            }
        )
    )

    user_handle = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'registration-input',
                'placeholder': '@',
                'name': 'user_handle'
            }
        )
    )   

    def clean_user_handle(self):
        user_handle = self.cleaned_data.get('user_handle', '').strip()

        print('user_handle', user_handle)

        user_handle = user_handle.lstrip('@')

        if not user_handle:
            print('Введить username')
            raise forms.ValidationError('Введить user_handle')
        
        if not re.fullmatch(r'[a-zA-Z0-9]+', user_handle):
            print("Тільки латиниця, цифри та '_'")
            raise forms.ValidationError("Тільки латиниця, цифри та '_'")

        user_handle = '@' + user_handle
            
        if Profile.objects.filter(pseudonym=user_handle).exists():
            print("Такий username вже зайнятий")
            raise forms.ValidationError('Такий username вже зайнятий') 

        print('user_handle', user_handle)

        return user_handle