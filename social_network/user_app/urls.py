from django.urls import path
from .views import *

urlpatterns = [
    path('auth/', AuthView.as_view(), name='auth'),
    path('confirm_email/', ConfirmEmaiView.as_view(), name='confirm_email'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

