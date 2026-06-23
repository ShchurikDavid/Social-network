from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', include('home_app.urls')),
    path('post/', include('post_app.urls')),
    path('chats/', include('chat_app.urls')),
    path('settings/', include('settings_app.urls')),
    path('friends/', include('profile_app.urls')),
    path('user/', include('user_app.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
