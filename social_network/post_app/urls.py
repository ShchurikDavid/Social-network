from django.urls import path
from .views import PostView, PostCreateView, TagCreateView, PostDeleteView, PostInteractView

urlpatterns = [
    path('', PostView.as_view(template_name='post_app/post.html'), name='post'),
    path('create_tag', TagCreateView.as_view(), name='create_tag'),
    path('creata_post', PostCreateView.as_view(), name='create_post'),
    path('interact_post/<str:interact_post>/<int:post_id>/', PostInteractView.as_view(), name='interact_post'),
    path('delete_post/<int:post_id>/', PostDeleteView.as_view(), name='delete_post')
]