from django.template.loader import render_to_string
from django.shortcuts import render
from django .views.generic import TemplateView, View, ListView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PostForm, TagForm
from .models import Tag, Post


class PostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post_app/post.html'
    paginate_by = 5
    context_object_name = 'posts'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # user_posts = Post.objects.filter(author=self.request.user).order_by('-create_at')[:2]
        # post_tags = Tag.objects.filter(posts__in=user_posts).distinct()
        # tag_list = list(Tag.objects.all()[:10]) + list(post_tags) + list(user_tags)

        context['tag_form'] = TagForm()
        context['post_form'] = PostForm()
        context['tags'] = unionTagList()
        
        return context
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest": 
            page_obj = context['page_obj']
            
            return JsonResponse({
                'posts_html': render_to_string(
                    'post_app/download_parts/post_list.html',
                    {"posts": context['posts']}      
                ),
                'has_next': page_obj.has_next()
            })
            
        return super().render_to_response(context, **response_kwargs)
    
    def get_queryset(self):   
        return (
            Post.objects.filter(author=self.request.user).
            select_related('author').
            prefetch_related('tags', 'links', 'images').
            order_by('-id')
        )


class TagCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('auth')

    def post(self, request, *args, **kwargs):
        form = TagForm(request.POST)

        if form.is_valid():
            tag = form.save()

            return JsonResponse({
                'success': True,
                'message': 'Публікація успішно створена',
                'tag_html': render_to_string('post_app/download_parts/post_form_tag.html', context={'tag': tag})
            })
    
        return JsonResponse({
            'success': False,
            'message': 'Публікація не була створена'
        })


class PostCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('auth')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs() 

        if self.request.method == "POST":
            kwargs['links'] = self.request.POST.getlist('links')
            kwargs['images'] = self.request.FILES.getlist('images')

        return kwargs
    
    def post(self, request, *args, **kwargs):
        form = PostForm(
            request.POST, 
            request.FILES,
            links=self.request.POST.getlist('links'),
            images=request.FILES.getlist('images')
        )

        print('form.is_valid()', form.is_valid())
        if form.is_valid():
            post = form.save(author=self.request.user)

            return JsonResponse({
                'success': True,
                'message': 'Публікація успішно створена',
                'post_html': render_to_string('post_app/download_parts/post_list.html', context={"posts": [post]})
            })
        
        print(form.errors)
        print(form.non_field_errors())
    
        return JsonResponse({
            'success': False,
            'message': 'Публікація не була створена'
        })


class PostInteractView(LoginRequiredMixin, View):
    def post(self, request, interact_post, post_id):
        post = Post.objects.get(id=post_id, author=request.user)
        do = post.toggleInteract(interact_post, request.user)
        return JsonResponse({'success': True, 'do': do})


class PostDeleteView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = Post.objects.get(id=post_id, author=request.user)
        post.delete()

        return JsonResponse({'success': True})


def unionTagList():
    return list(Tag.objects.order_by('id')[:10])