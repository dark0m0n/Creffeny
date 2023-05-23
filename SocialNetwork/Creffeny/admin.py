from django.contrib import admin

from Creffeny.models import Post, Comment

# Register your models here.
@admin.register(Post)
class Admin(admin.ModelAdmin):
    list_display = ['user', 'title', 'body', 'image', 'created_at', 'modified_at']


@admin.register(Comment)
class Admin(admin.ModelAdmin):
    list_display = ['user', 'body']
