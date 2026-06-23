from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

from .load_msg import get_msg_list
from ..models import Chat
from user_app.models import User
from profile_app.models import Profile
from profile_app.services.freind_qureist import get_friends

def friends_pages(friends_list):
    sorted_friends = sorted(friends_list, key=lambda friend: friend.profile.pseudonym)
    
    last_leter = None
    all_friends = []
    
    for friend in sorted_friends:
        if last_leter != friend.profile.pseudonym[0]:
            all_friends.append({
                "letter": friend.profile.pseudonym[0]
            })
            
            last_leter = friend

        all_friends.append(friend)

    return all_friends

def create_group(request):
    file = request.FILES.get('file')
    name = request.POST.get("name", "").strip()
    user_ids = request.POST.getlist("users")

    if not name:
        return JsonResponse({'success': False, "error": "name_required"}, status=400)
    
    if len(user_ids) <= 1:
        return JsonResponse({'success': False, "error": "add_users"}, status=400)
    
    friend_ids = get_friends(request.user).filter(id__in=user_ids).values_list("id", flat=True)
    chat = Chat.objects.create(name=name, is_group=True, admin=request.user)
    chat.avatar = file if file else 'profiles/avatars/chat_img.svg'
    chat.users.add(request.user)
    chat.users.add(*User.objects.filter(id__in=friend_ids))

    return JsonResponse({'success': True, 'chat_id': chat.id, "name": chat.name, 'chat_html':  render_to_string(
                        'chat_app/particals/groups.html',
                        {"groups": [chat]}      
                    ),})
    

def edit_create_group(request, chat_id):
    name = request.POST.get("name", "").strip()
    user_ids = request.POST.getlist("users")

    if not name:
        return JsonResponse({'success': False, "error": "name_required"}, status=400)
    
    if len(user_ids) <= 1:
        return JsonResponse({'success': False, "error": "add_users"}, status=400)
    
    friend_ids = get_friends(request.user).filter(id__in=user_ids).values_list("id", flat=True)
    chat = get_object_or_404(Chat, id=chat_id)

    chat.name = name
    chat.users.clear()
    chat.users.add(request.user)
    chat.users.add(*User.objects.filter(id__in=friend_ids))

    chat.save()

    other_user = chat.users.exclude(id=request.user.id).first()
    messages = chat.messages.all().order_by('-created_at')[:20]
    messages = reversed(messages)
    chat_messages = get_msg_list(messages)
        
    return JsonResponse({'success': True, 'chat_id': chat.id, "name": chat.name, 'group_html':  render_to_string(
        'chat_app/particals/chat_messages.html',
        {'chat': chat, 'chat_users': chat.users.all(), 'other_user': other_user, 'chat_messages': chat_messages, 'user': request.user})     
    })

    return JsonResponse({'success': False})