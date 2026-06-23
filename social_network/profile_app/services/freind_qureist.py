from user_app.models import User
from profile_app.models import Profile

def get_friendship_requests(current_user: User, filter_input: str = ''):
    return User.objects.filter(
        sent_friendships__to_user=current_user, 
        sent_friendships__status='pending',
        username__icontains=filter_input
    ).order_by("id")

def get_friendship_recommendation(current_user: User, filter_input: str = ''):
    sent_busy_ids = list(current_user.sent_friendships.
                         values_list("to_user_id", flat=True))
    
    received_busy_ids = list(current_user.received_friendships.
                             values_list("from_user_id", flat=True))
    
    busy_ids = sent_busy_ids + received_busy_ids + [current_user.id]

    return User.objects.exclude(id__in=busy_ids).filter(username__icontains=filter_input).order_by("id")
    

def get_friends(current_user: User, filter_input: str = ''):
    sent_friends = list(current_user.sent_friendships.filter(status="accepted").
                           values_list("to_user_id", flat=True))
    
    received_friend_ids = list(current_user.received_friendships.filter(status="accepted").
                         values_list("from_user_id", flat=True))
    friend_ids = sent_friends + received_friend_ids
    
    return User.objects.filter(id__in=friend_ids).filter(username__icontains=filter_input).order_by("id")