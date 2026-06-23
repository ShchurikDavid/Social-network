from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.template.loader import render_to_string

from .forms import ProfileForm
from post_app.forms import PostForm, TagForm
from user_app.models import User, Friendship
from post_app.models import Post
from chat_app.models import Chat, Message
from profile_app.models import Profile
from post_app.views import unionTagList

from profile_app.services.freind_qureist import get_friends, get_friendship_recommendation, get_friendship_requests

def all_chat():
    print('start =====================')

    for chat in Chat.objects.all():
        chat.avatar = 'profiles/avatars/chat_img.svg'
        chat.save()

def all_users(me):
    for user in Profile.objects.all():
        # if user.id != me.id:
            # user.signature = 'profiles/signatures/avatar_sing.svg'

            user.is_image_signature = True
            user.is_text_signature = True
            user.save()

def del_chat():
    chats_list = []

    for chat_id in chats_list:
        chat = Chat.objects.get(id=chat_id)
        if chat:
            chat.delete()

class HomeView(ListView):
    model = Post
    paginate_by = 5
    context_object_name = 'posts'
    template_name = 'home_app/home.html'
    form_class = ProfileForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        first_registration = self.request.session.get('first_registration')
        if first_registration != None and first_registration != '':
            first_registration = True

        # all_chat()
        # all_users(self.request.user)
        context['first_registration'] = first_registration
        context['modal_form'] = self.form_class
        context['friends_count'] = Friendship.objects.filter(to_user=self.request.user, status="accepted").count()
        context['tag_form'] = TagForm()
        context['post_form'] = PostForm()

        try:
            context['tags'] = unionTagList()
        except Profile.DoesNotExist:
            print('Profile does not exist')

        for post in context['posts']:
            post.toggleInteract('views', self.request.user)

        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            user_data = form.cleaned_data
            user = User.objects.filter(email=request.session.get('first_registration')).first()
            
            if user:    
                print(1, user_data['user_handle'], user_data['username'])
                user.username = user_data['user_handle']
                user.save()

                profile = Profile.objects.create(
                    user = user,
                    pseudonym = user_data['username']
                )
                
                request.session.pop('first_registration', None)

                # return redirect('home')

                return JsonResponse({
                    'success': True,
                    'username': profile.pseudonym,
                    'pseudonym': user.username, 
                })
            
        return JsonResponse({  
            'success': False, 
            'error': form.errors
        }, status=400)
        

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest": 
            page_obj = context['page_obj']
            posts = context['posts']

            for post in posts:
                post.toggleInteract('views', self.request.user)
            
            return JsonResponse({
                'posts_html': render_to_string(
                    'post_app/download_parts/post_list.html',
                    {"posts": posts}      
                ),
                'has_next': page_obj.has_next()
            })
            
        return super().render_to_response(context, **response_kwargs)
    
    def get_queryset(self):   
        return (
            Post.objects.select_related('author').
            prefetch_related('tags', 'links', 'images').
            order_by('-id')
        )
    
class HomeLoaderView(LoginRequiredMixin, View):
    def get(self, context, **response_kwargs):
        selection = self.request.GET.get('selection', 0)

        if selection == 'requests':
            friends_count_list = []
            requests = get_friendship_requests(self.request.user)[:3]

            for user in requests:
                friends_count_list.append(Friendship.objects.filter(to_user=user, status="accepted").count())
                
            return JsonResponse({
                'chats_html': render_to_string(
                    'home_app/particals/requests.html',
                    {"requests": get_friendship_requests(self.request.user)[:3], 'user_profile': self.request.user.profile, 'friends_count_list': friends_count_list}      
                )
            })
        elif selection == 'chats':
            messages_prefetch = Prefetch('messages',queryset=Message.objects.order_by('-created_at'))
            chats = Chat.objects.filter(users=self.request.user, is_group = False).prefetch_related(messages_prefetch).order_by("id")[:3]
            print('chats', chats)
            return JsonResponse({
                'chats_html': render_to_string(
                    'home_app/particals/chats.html',
                    {"chats": chats, 'user': self.request.user}      
                )
            })
    
        return super().render_to_response(context, **response_kwargs)