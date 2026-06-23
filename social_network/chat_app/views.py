from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Prefetch
from django.http import HttpRequest
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone


from .models import Chat, Message, MessageImage
from profile_app.models import Profile
from user_app.models import User
from .services.load_msg import get_msg_list
from .services.add_group_page import friends_pages, create_group, edit_create_group
from profile_app.services.freind_qureist import get_friends
from profile_app.services.freind_qureist import *


class ChatView(TemplateView):
    template_name = 'chat_app/chat.html'


    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        # friends_list = get_friends(self.request.user)
        # context["all_friends"] = friends_pages(friends_list) 
        # context['user_profile'] = self.request.user.profile
        # context['friends'] = friends_list[:12]
        # context["chats"] = Chat.objects.filter(users=self.request.user, is_group = False).order_by("id")[:7]
        # context['groups'] = Chat.objects.filter(users=self.request.user, is_group = True).order_by("id")
        
        return context
    

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest": 
            paginator_list = []
            users_list = []
            paginato_page = int(self.request.GET.get('page', 1))
            filter_text = self.request.GET.get('filter_text', '')
            selection = self.request.GET.get('selection', 0)

            messages_prefetch = Prefetch('messages',queryset=Message.objects.order_by('-created_at'))
            if selection == 'friends':
                paginator_list = get_friends(self.request.user, filter_text)
            elif selection == 'chats':
                paginator_list = Chat.objects.filter(users=self.request.user, is_group = False).prefetch_related(messages_prefetch).order_by("id")
                for chat in paginator_list:
                    for user in chat.users.all():
                        if user.id != self.request.user.id:
                            users_list.append(user.id)
            elif selection == 'groups':
                paginator_list = Chat.objects.filter(users=self.request.user, is_group = True).prefetch_related(messages_prefetch).order_by("id")

            page_obj = Paginator(paginator_list, 12 if selection == 'friends' else 7).get_page(paginato_page)
            
            if selection == 'friends':
                return JsonResponse({
                    'friends_html': render_to_string(
                        'chat_app/particals/friends.html',
                        {"friends": page_obj}      
                    ),
                    'friends_ids': list(user.id for user in paginator_list),
                    'has_next': page_obj.has_next()
                })
            elif selection == 'chats':
                return JsonResponse({
                    'chats_html': render_to_string(
                        'chat_app/particals/chats.html',
                        {"chats": page_obj, 'user': self.request.user}      
                    ),
                    'friends_ids': users_list,
                    'has_next': page_obj.has_next()
                })
            elif selection == 'groups':
                if int(paginato_page) == page_obj.number:
                    return JsonResponse({
                        'groups_html': render_to_string(
                            'chat_app/particals/groups.html',
                            {"groups": page_obj, 'user_profile': self.request.user}      
                        ),
                        'has_next': page_obj.has_next()
                    })         
            elif selection == 'messages':
                chat = Chat.objects.get(id=int(self.request.GET.get('chat_id', None)))

                if chat:
                    messages_list = chat.messages.order_by('-created_at')
                    page_obj = Paginator(messages_list, 20).get_page(paginato_page)

                    if int(page_obj.number) == paginato_page:
                        messages = reversed(page_obj.object_list)
                        messages_with_dates = get_msg_list(messages)

                        return JsonResponse({
                            'messages_html': render_to_string(
                                'chat_app/chat_msg/msg.html',
                                {'chat_messages': messages_with_dates, 'user': self.request.user}
                            ),
                            'has_next': page_obj.has_next()
                        })

        return super().render_to_response(context, **response_kwargs)
    
class ChatModalView(View):    
    def get(self, context, **response_kwargs):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest": 
            paginato_page = int(self.request.GET.get('page', 1))
            filter_text = self.request.GET.get('filter_text', '')
            edit_modal = str(self.request.GET.get('edit_modal', 'false')) == 'true'
            friends_list = get_friends(self.request.user, filter_text)
            all_friends = friends_pages(friends_list) 

            page_obj = Paginator(all_friends, 20).get_page(paginato_page)

            return JsonResponse({
                'html': render_to_string(
                    'chat_app/modals/user_array.html',
                    {'all_friends': page_obj, 'user': self.request.user, 'edit_modal': edit_modal}
                ),
                'has_next': page_obj.has_next()
            })

        return JsonResponse({"error": "Bad request"}, status=400)

class ChatWithView(LoginRequiredMixin, View):
    login_url = reverse_lazy("auth")


    def post(self, request, user_id, *args, **kwargs):
        add_new_user = False
        current_user = request.user
        other_user = User.objects.get(id = user_id)

        friends = get_friends(current_user)

        if other_user not in friends:
            return JsonResponse({"success": False}, status=403)
        
        user_chat_ids = Chat.objects.filter(users=current_user, is_group=False).values_list("id", flat=True)
        chat = Chat.objects.filter(id__in = user_chat_ids, users=other_user, is_group=False).first()

        if chat is None:
            add_new_user = True
            chat = Chat.objects.create(is_group=False)
            chat.users.add(current_user, other_user)
        
        return JsonResponse({
            "success": True, 
            'chats_html': render_to_string(
                    'chat_app/particals/chats.html',
                    {"chats": [chat if add_new_user else []], 'user': self.request.user}      
                ),
            "chat_id": chat.id
        })
    

class CreateGroupView(LoginRequiredMixin, View):
    login_url = reverse_lazy("auth")
    

    def post(self, request):
        return create_group(request)
    
class EditGroupView(LoginRequiredMixin, View):
    login_url = reverse_lazy("auth")
    

    def post(self, request, chat_id):
        return edit_create_group(request, chat_id)

     
class ChatMessageWithImages(LoginRequiredMixin, View):
    login_url = reverse_lazy('auth')
    

    def post(self, request: HttpRequest, chat_id):
        if not Chat.objects.filter(id=chat_id, users=request.user).exists():
            return JsonResponse({"success": False}, status=403)
        
        text = request.POST.get("text", "").strip()
        images = request.FILES.getlist("images")

        if not text and not images:
            return JsonResponse({"success": False}, status=400)
        
        message_list = []
        message = Message.objects.create(chat_id=chat_id, sender=request.user, text=text)
        
        for image in images:
           msg = MessageImage.objects.create(message=message, image=image)
           print(msg.image.url) 
           message_list.append(msg.get_json())

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f'chat{chat_id}',
            {
                'type': 'send_chat_message',
                'message_id': message.id,
                'input_message': message.text,
                'message_images': message_list,
                'sender': request.user.username,
                'my_msg_html': render_to_string(
                    'chat_app/chat_msg/my_msg.html',
                    {'msg': message, 'user': request.user.username}      
                ),
                'other_msg_html': render_to_string(
                    'chat_app/chat_msg/other_msg.html',
                    {'msg': message, 'user': request.user.username}      
                )
            }
        )

        return JsonResponse({'success': True})