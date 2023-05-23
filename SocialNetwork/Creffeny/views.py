from django.shortcuts import render

from Creffeny.models import Post, Comment, Like
from Creffeny.forms import Registration

from django.urls import reverse_lazy

from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView


class IndexView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creffeny'
        context['user'] = self.request.user
        return context


class PostView(TemplateView):
    template_name = 'posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs['pk'])
        context['post'] = post
        comment = Comment.objects.filter(post=post)
        context['comments'] = comment
        context['title'] = f'Creffeny - {post.title}'
        context['like_amount'] = len(Like.objects.filter(post=post))
        return context

    def post(self, request, **kwargs):
        data = request.POST
        user = self.request.user
        post = Post.objects.get(id=self.kwargs['pk'])


class Register(CreateView):
    form_class = Registration
    template_name = 'registration.html'
    success_url = reverse_lazy('login')

    
class Login(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


class Logout(LogoutView):
    pass


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['posts'] = Post.objects.filter(user=user)
        context['title'] = 'Profile'
        return context
