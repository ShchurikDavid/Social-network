from django.urls import path
from .views import HomeView, HomeLoaderView

urlpatterns = [
    path('', HomeView.as_view(template_name = 'home_app/home.html'), name="home"),
    path('home_loder', HomeLoaderView.as_view(), name='home_loader')
]