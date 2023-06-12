from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=1250)
    image = models.ImageField(upload_to='static/post_images', validators=[FileExtensionValidator(['jpg', 'png'])])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.CharField(max_length=350)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)


class ProfileImage(models.Model):
    profile_image = models.ImageField(upload_to='static/profile_images', validators=[FileExtensionValidator(['jpg', 'png'])], default='static/icons/user.png')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


@receiver(models.signals.post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        ProfileImage.objects.create(user=instance, profile_image='static/icons/user.png')
