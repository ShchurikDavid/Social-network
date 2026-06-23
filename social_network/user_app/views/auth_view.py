from django.views.generic import TemplateView
from django.http import  HttpRequest
from ..forms.login_form import LoginForm
from ..forms.confirm_email_form import ConfirmEmail
from ..forms.registration_form import RegistrationForm


class AuthView(TemplateView):
    template_name = 'user_app/auth.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['confirm_email_form'] = ConfirmEmail()
        context['registration_form'] = RegistrationForm()
        context['login_form'] = LoginForm()
        
        return context
