from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError

from django.conf import settings

def send_email_code(email, code):
    subject = "Пробное заголовок"
    message = f"Пробное текст, код: {code}"
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email]
        )
    except BadHeaderError:
        return HttpResponse('Найден некорректный заголовок')
