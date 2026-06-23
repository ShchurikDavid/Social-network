from django.urls import path
from .views import *

urlpatterns = [
    path('profile/<int:user_id>/<str:action>', ProfileView.as_view(template_name = 'profile_app/profile.html'), name="profile"),
    path('all_friends', AllFriendsView.as_view(template_name = 'friends_app/friends.html'), name="all_friends"),
    path('all_friends/<str:selection>', FriendsSelectionView.as_view(), name="all_friends_selection"),
    path('friends_action/<str:action>/<int:profile_id>', FriendsAction.as_view(), name="friends_action")
]