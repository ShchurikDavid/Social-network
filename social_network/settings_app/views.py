from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import update_session_auth_hash
from django import forms
import re

from user_app.models import User
from home_app.forms import ProfileForm
from profile_app.models import Profile


def clean_username(username, user):
    username = (username or '').strip()
    print('user_handle', username)

    username = username.lstrip('@')

    if not username:
        raise ValueError('Введіть user_handle')

    if not re.fullmatch(r'[a-zA-Z0-9_]+', username):
        raise ValueError("Тільки латиниця, цифри та _")

    username = '@' + username

    if User.objects.exclude(id=user.id).filter(username=username).exists():
        raise ValueError('Такий username вже зайнятий')

    print('user_handle', username)

    return username

class SettingsView(TemplateView):
    template_name = 'settings_app/settings.html'


class SettingsSaveView(View):
    def post(self, request, action, *args, **kwargs):
        user = request.user
        profile = user.profile

        if action == 'pictire_set':
            print('pictire_set', user)

            avatar = request.FILES.get('avatar')

            if (avatar):
                profile.avatar = avatar

            user.username = clean_username(request.POST.get('username', user.username), user)

            user.save()
            profile.save()

            return JsonResponse({'success': True, 'username': user.username, 'avatar_url': profile.avatar.url })

        elif action == 'base_set':
            user.email = request.POST.get('email', user.email)
            print('last_name', request.POST.get('last_name', 'Прізвище'))
            profile.pseudonym = request.POST.get('pseudonym', user.profile.pseudonym)

            birth_date = request.POST.get('birth_date')
            if birth_date:
                profile.birth_date = birth_date

            user.save()
            profile.save()

            return JsonResponse({'success': True, 'pseudonym': profile.pseudonym, 'birth_date': profile.birth_date, 'email': user.email }) 
        elif action == 'password_set':
            my_password = request.POST.get('my_password')
            new_password = request.POST.get('new_password')
            check_password = request.POST.get('check_password')

            if not new_password or not check_password or not my_password:
                return JsonResponse({'success': False}, status=400) 
            
            if new_password != check_password:
                return JsonResponse({'success': False}, status=400) 
            
            if request.user.check_password(my_password):
                user.set_password(new_password)
                user.save()

                update_session_auth_hash(request, user)

                return JsonResponse({'success': True}) 
        elif action == 'sing_set':
            avatar = request.POST.get('avatar') == 'true'
            signature = request.POST.get('signature') == 'true'

            print(avatar, signature, 'signature')
            profile.is_text_signature = avatar
            profile.is_image_signature = signature
            profile.save()

            return JsonResponse({'success': True}) 
            
        return JsonResponse({'success': False}, status=400) 

    