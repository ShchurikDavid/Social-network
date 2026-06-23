from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

from user_app.models import User
from profile_app.models import Profile


class Tag(models.Model):
    name = models.CharField(max_length=100)
    # author = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)=

    def __str__(self):
        return self.name
    

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255, null=True)
    tags = models.ManyToManyField(Tag, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, blank=True, null=True)

    
    def __str__(self):
        return self.title

    def toggleInteract(self, interact, profile):
        print("addHeart", interact, profile)

        toggle = self.hasInteract(interact, profile)
        
        if interact == 'likes':
            if (toggle):
                PostLike.objects.filter(user=profile, post=self).delete()
                print('delete PostLike')
                return False
            PostLike.objects.create(user=profile, post=self)
        elif interact == 'hearts':
            if (toggle):
                PostHeart.objects.filter(user=profile, post=self).delete()
                print('delete PostHeart')
                return False
            PostHeart.objects.create(user=profile, post=self)
        elif interact == 'views':
            if (toggle): return False
            PostView.objects.create(user=profile, post=self)

        return True
    
    
    def hasInteract(self, interact, profile):
        print("hasInteract", interact, profile)
        return getattr(self, interact).filter(user=profile).exists()
    

class PostLike(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='liked_posts')
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_post_like'
            )
        ]

class PostHeart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='hearted_posts')
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='hearts')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_post_hearts'
            )
        ]

class PostView(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='viewed_posts')
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='views')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_post_view'
            )
        ]

class PostLink(models.Model):
    url = models.URLField()
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='links')


class PostImage(models.Model):
    original_image = models.ImageField(blank=True, upload_to="media/post_app/original_images")
    compressed_image = models.ImageField(blank=True, upload_to="media/post_app/compressed_images")
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.original_image.name

