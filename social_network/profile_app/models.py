from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from user_app.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, null=True)
    birth_date = models.DateField(null=True, blank=True)
    signature = models.ImageField(upload_to='media/profile_app/signatures', null=True, blank=True)
    avatar = models.ImageField(upload_to='media/profile_app/avatars', null=True, blank=True)
    pseudonym = models.CharField(max_length=50, null=True, blank=True)
    is_image_signature = models.BooleanField(default=False)
    is_text_signature = models.BooleanField(default=False)

    # friends = models.ManyToManyField('self', blank=True, verbose_name="Друзі")

    def __str__(self):
        return f"Профіль: {self.user.username}"

class Album(models.Model):
    name = models.CharField(max_length=100)
    theme = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='albums')
    is_shown = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
class AlbumImage(models.Model):
    image = models.ImageField(upload_to='media/profile_app/albums')
    album = models.ForeignKey(to=Album, on_delete=models.CASCADE, related_name='images')
    is_shown = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Фото для альбому {self.album.name}"
    