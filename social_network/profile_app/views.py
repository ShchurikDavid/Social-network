from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.template.loader import render_to_string


from user_app.models import User, Friendship
from profile_app.models import Profile
from post_app.forms import PostForm
from post_app.models import Post
from .services.freind_action import *
from .services.freind_qureist import get_friends, get_friendship_recommendation, get_friendship_requests


class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'profile_app/profile.html'
    form_class = PostForm
    paginate_by = 6
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth')
        
        if not User.objects.filter(id=self.kwargs.get('user_id')).exists():
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        first_registration = self.request.session.get('first_registration')
        if first_registration != None and first_registration != '':
            first_registration = True

        context['first_registration'] = first_registration
        context['modal_form'] = self.form_class
        context['select_user'] = User.objects.filter(id=self.kwargs.get('user_id')).first()
        context['action'] = self.kwargs.get('action')

        for post in context['posts']:
            post.toggleInteract('views', self.request.user)
        
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
                
            return JsonResponse({
                'success': True
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
            Post.objects.filter(author=User.objects.filter(id=self.kwargs.get('user_id')).first()).
            select_related('author').
            prefetch_related('tags', 'links', 'images').
            order_by('-id')
        )


class AllFriendsView(LoginRequiredMixin, TemplateView):
    template_name = 'friends_app/friend.html'
    login_url = reverse_lazy('auth')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context['requests'] = get_friendship_requests(self.request.user)[:3]
        # context['recommendations'] = get_friendship_recommendation(self.request.user)[:6]
        # context['friend'] = get_friends(self.request.user)[:6]

        return context
    
    # def post(self, request, type, *args, **kwargs):
    #     friends_list = []

    #     if type == 'requests':
    #         friends_list = get_friendship_requests(self.request.user)[:3]
    #     elif type == 'recommendations':
    #         friends_list = get_friendship_recommendation(self.request.user)[:6]
    #     elif type == 'friend':
    #         friends_list = get_friends(self.request.user)[:6]

    #     return JsonResponse(friends_list)


class FriendsAction(LoginRequiredMixin, TemplateView):
    def post(self, request, action, profile_id, *args, **kwargs):
        other_user_profile = User.objects.get(id=profile_id)

        if action == 'accept':
            result = accept_friend_request(request.user, other_user_profile)

            return JsonResponse(result)
        elif action == 'request':
            result = add_friend_request(request.user, other_user_profile)

            return JsonResponse(result)
        elif action == 'delete_frienship':
            result = delete_friendship(request.user, other_user_profile)

            return JsonResponse(result)
        elif action == 'dismissed':
            result = dismiss_recommendation(request.user, other_user_profile)

            return JsonResponse(result)
        
        return JsonResponse({'success': False})


    
class FriendsSelectionView(LoginRequiredMixin, View):
    def get(self, request, selection, *args, **kwargs ):
        limit = int(request.GET.get('limit', 0))
        filter_input = request.GET.get('filter_text', '')
        user = [] 
        html = ''

        if selection == 'requests':
            user = get_friendship_requests(request.user, filter_input)
        elif selection == 'recommendations':
            user = get_friendship_recommendation(request.user, filter_input)
        elif selection == 'friend':
            user = get_friends(request.user, filter_input)

        page_obj = Paginator(user, limit if limit else 6).get_page(request.GET.get('page', 1))

        if (page_obj.number == int(request.GET.get('page', 1))):
            html = render_to_string( 
                f"friends_app/particals/{selection}.html",
                {selection: page_obj.object_list},
                request=request
            )
        
        return JsonResponse({"html": html, "has_next_page": page_obj.has_next()})
