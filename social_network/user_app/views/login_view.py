from django.http import JsonResponse, HttpRequest
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView

from ..models import User
from ..forms.login_form import LoginForm


class LoginPageView(LoginView):
    form_class = LoginForm

    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            print('form', form, form.user)
            login(request, form.user)
            return JsonResponse({'success': True})
        
        return JsonResponse({'success': False, 'error': form.errors}, status=400)
        

class LogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')