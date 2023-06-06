from django.shortcuts import render

from Creffeny.models import Post, Comment, Like
from Creffeny.forms import Registration, LoginForm

from django.urls import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LogoutView, LoginView

import time


class IndexView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creffeny'
        context['user'] = self.request.user
        return context


class AddPostView(TemplateView):
    def post(self, request):
        data = request.FILES['file']
        post = request.POST
        user = self.request.user
        now = round(time.time()*10000)
        if 'formd' in post.keys():
            with open(f'static/post_images/{now}.png', 'wb') as file:
                file.write(data.read())
                return JsonResponse(f'/static/post_images/{now}.png', safe=False)
        
        if 'title' in post.keys() and 'body' in post.keys():
            with open(f'static/post_images/{now}.png', 'r') as file:
                p = Post(user=user,
                    image=file,
                    title=post['title'],
                    body=post['body'])
                p.save()       


class PostView(TemplateView):
    template_name = 'posts.html'

    def post(self, request, **kwargs):
            data = request.POST
            user = self.request.user
            post = Post.objects.get(id=self.kwargs['pk'])

            if 'text' in data.keys():
                comment = Comment(user=user, post=post, body=data['text'])
                comment.save()
                result = render_to_string('comment.html', {'user': user, 'comment': comment})
                return JsonResponse(result, safe=False)
            
            if 'like' in data.keys():
                likes = Like.objects.filter(post=post)
                for like in likes:
                    if like.user == user:
                        like.delete()
                        like_info = 0
                        break
                else:
                    like = Like(user=user, post=post)
                    like.save()
                    like_info = 1
                return JsonResponse({'like_amount': len(Like.objects.filter(post=post)), 'is_like': like_info}, safe=False)
            
            if 'is_like' in data.keys():
                likes = Like.objects.filter(post=post)
                for like in likes:
                    if like.user == user:
                        return JsonResponse({'is_like': 1}, safe=False)
                else:
                    return JsonResponse({'is_like': 0}, safe=False)        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs['pk'])
        comment = Comment.objects.filter(post=post)
        context['post'] = post
        context['comments'] = comment
        context['title'] = f'Creffeny - {post.title}'
        context['like_amount'] = len(Like.objects.filter(post=post))
        return context


class Register(CreateView):
    form_class = Registration
    template_name = 'registration.html'
    success_url = reverse_lazy('login')

    
class Login(LoginView):
    form_class = LoginForm
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
