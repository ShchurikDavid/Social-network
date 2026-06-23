from django.conf import settings

def app_settings(request):
    return {'LOCAL': settings.LOCAL,}