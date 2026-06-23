from django.urls import reverse_lazy
from django.http import JsonResponse, HttpRequest
from django.views.generic import CreateView
from ..forms.registration_form import RegistrationForm

from ..models import User
from ..services.auth_service import save_registration


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user_data = form.cleaned_data
            save_registration(request=request, cleaned_data=user_data)
            request.session['first_registration'] = user_data['email']
            
            return JsonResponse({'success': True})
        
        return JsonResponse({'success': False, 'error': form.errors}, status=400)