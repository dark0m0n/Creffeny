from django.shortcuts import render

from Creffeny.models import Post, Comment, Like, ProfileImage
from Creffeny.forms import Registration, LoginForm
from django.contrib.auth.models import User

from django.urls import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.files import File

from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LogoutView, LoginView

from pathlib import Path


class IndexView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creffeny'
        context['user'] = self.request.user
        context['profile'] = ProfileImage.objects.get(user=self.request.user)
        return context


class AddPostView(TemplateView):
    def post(self, request):
        user = self.request.user
        posts_len = len(Post.objects.all())
        image = f'static/post_images/{user}_{posts_len}.png'
        data = request.POST
        if 'body' in data.keys():
            body = data['body']
            title = data['title']
            path = Path(image)
            with path.open(mode='rb') as f:
                file = File(f, name=path.name)
                post = Post(body=body, image=file, title=title, user=user)
                post.save()
        if 'formd' in data.keys():
            data = request.FILES['file']
            with open(image, 'wb') as file:
                file.write(data.read())
        return JsonResponse(image, safe=False)


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
    template_name = 'login.html'
    redirect_authenticated_user = True
    form_class = LoginForm


class Logout(LogoutView):
    pass


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs['username'])
        context['user'] = user
        context['posts'] = Post.objects.filter(user=user)
        context['profile'] = ProfileImage.objects.get(user=user)
        return context

    def post(self, request, **kwargs):
        pass
