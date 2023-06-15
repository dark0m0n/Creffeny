from django.shortcuts import render

from Creffeny.models import Post, Comment, Like, ProfileImage, Dislike, Chat, Message
from Creffeny.forms import Registration, LoginForm, ChatForm
from django.contrib.auth.models import User

from django.urls import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.files import File

from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.list import ListView
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LogoutView, LoginView

from pathlib import Path
import random


@method_decorator(login_required(login_url='/registration'), name='dispatch')
class IndexView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creffeny'
        context['user'] = self.request.user
        context['profile'] = ProfileImage.objects.get(user=self.request.user)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        posts = list(queryset)
        random.shuffle(posts)
        return posts


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


@method_decorator(login_required(login_url='/registration'), name='dispatch')
class PostView(LoginRequiredMixin, TemplateView):
    template_name = 'posts.html'

    def post(self, request, **kwargs):
            data = request.POST
            user = self.request.user
            post = Post.objects.get(id=self.kwargs['pk'])

            if 'text' in data.keys():
                if data['text'] == '':
                    pass
                else:
                    comment = Comment(user=user, post=post, body=data['text'])
                    comment.save()
                    result = render_to_string('comment.html', {'c': comment})
                    return JsonResponse(result, safe=False)
            
            if 'like' in data.keys():
                likes = Like.objects.filter(post=post)
                dislikes = Dislike.objects.filter(post=post)
                for like in likes:
                    if like.user == user:
                        like.delete()
                        like_info = 0
                        for dislike in dislikes:
                            if dislike.user == user:
                                dislike_info = 1
                                break
                        else:
                            dislike_info = 0
                        break
                else:
                    like = Like(user=user, post=post)
                    like.save()
                    like_info = 1
                    for dislike in dislikes:
                        if dislike.user == user:
                            dislike.delete()
                            dislike_info = 0
                            break
                    else:
                        dislike_info = 0
                return JsonResponse(
                    {
                        'like_amount': len(Like.objects.filter(post=post)),
                        'is_like': like_info,
                        'dislike_amount': len(Dislike.objects.filter(post=post)),
                        'is_dislike': dislike_info
                    },
                    safe=False
                )

            if 'dislike' in data.keys():
                likes = Like.objects.filter(post=post)
                dislikes = Dislike.objects.filter(post=post)
                for dislike in dislikes:
                    if dislike.user == user:
                        dislike.delete()
                        dislike_info = 0
                        for like in likes:
                            if like.user == user:
                                like_info = 1
                                break
                        else:
                            like_info = 0
                        break
                else:
                    dislike = Dislike(user=user, post=post)
                    dislike.save()
                    dislike_info = 1
                    for like in likes:
                        if like.user == user:
                            like.delete()
                            like_info = 0
                            break
                    else:
                        like_info = 0
                return JsonResponse(
                    {
                        'dislike_amount': len(Dislike.objects.filter(post=post)),
                        'is_dislike': dislike_info,
                        'like_amount': len(Like.objects.filter(post=post)),
                        'is_like': like_info
                    },
                    safe=False
                )

            if 'is_like' in data.keys():
                likes = Like.objects.filter(post=post)
                for like in likes:
                    if like.user == user:
                        return JsonResponse({'is_like': 1}, safe=False)
                else:
                    return JsonResponse({'is_like': 0}, safe=False)

            if 'is_dislike' in data.keys():
                dislikes = Dislike.objects.filter(post=post)
                for dislike in dislikes:
                    if dislike.user == user:
                        return JsonResponse({'is_dislike': 1}, safe=False)
                else:
                    return JsonResponse({'is_dislike': 0}, safe=False)

            if 'comment_like' in data.keys():
                comment = Comment.objects.get(id=data['comment_id'])
                likes = Like.objects.filter(comment=comment)
                for like in likes:
                    if like.user == user:
                        like.delete()
                        clike_info = 0
                        break
                else:
                    like = Like(user=user, comment=comment)
                    like.save()
                    clike_info = 1
                return JsonResponse(
                    {
                        'comment_like_amount': len(Like.objects.filter(comment=comment)),
                        'is_comment_like': clike_info
                    },
                    safe=False
                )

            if 'is_comment_like' in data.keys():
                comment = Comment.objects.get(id=data['comment_id'])
                likes = Like.objects.filter(comment=comment)
                for like in likes:
                    if like.user == user:
                        return JsonResponse({'is_comment_like': 1}, safe=False)
                else:
                    return JsonResponse({'is_comment_like': 0}, safe=False)

            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs['pk'])
        comment = Comment.objects.filter(post=post)
        context['post'] = post
        context['comments'] = comment
        context['title'] = f'Creffeny - {post.title}'
        context['like_amount'] = len(Like.objects.filter(post=post))
        context['profile'] = ProfileImage.objects.get(user=self.request.user)
        context['post_profile'] = ProfileImage.objects.get(user=post.user)
        context['dislike_amount'] = len(Dislike.objects.filter(post=post))
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


@method_decorator(login_required(login_url='/registration'), name='dispatch')
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs['username'])
        context['user'] = user
        context['posts'] = Post.objects.filter(user=user)
        context['profile'] = ProfileImage.objects.get(user=self.request.user)
        context['p_profile'] = ProfileImage.objects.get(user=user)
        if user == self.request.user:
            context['change_profile'] = 'Change image'
            context['change_profile_id'] = 'change_img'
        else:
            context['change_profile'] = 'Message'
            context['change_profile_id'] = 'messageto'
        return context

    def post(self, request, **kwargs):
        pass


class ChengeProfileImage(UpdateView):
    model = ProfileImage
    def post(self, request):
        data = request.POST
        user = self.request.user
        image = f'static/profile_images/{user}_profile.png'

        if 'changed' in data.keys():
            path = Path(image)
            with path.open(mode='rb') as f:
                file = File(f, name=path.name)
                profile = ProfileImage.objects.get(user=user)
                profile.profile_image = file
                profile.save()
        if 'change_img' in data.keys():
            data = request.FILES['file']
            with open(image, 'wb') as file:
                file.write(data.read())
        return JsonResponse(image, safe=False)


class StartChatView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        user1 = User.objects.get(id=self.kwargs['user_id'])
        for c in Chat.objects.all():
            if user in c.members.all() and user1 in c.members.all():
                self.url = '/chats'
                break
        else:
            chat = Chat()
            chat.save()
            chat.members.add(user, user1)
            self.url = '/chats'
        return super().get_redirect_url(*args, **kwargs)


class ChatsView(TemplateView):
    template_name = 'chats.html'

    def post(self, request):
        data_post = request.POST
        user = self.request.user
        chat = Chat.objects.get(id=data_post['chat'])
        if 'message' in data_post.keys():
            message = Message(user=user, chat=chat, body=data_post['message'])
            message.save()
            return JsonResponse({'message': message.body}, safe=False)
        messages = Message.objects.filter(chat=chat)
        form = ChatForm()
        result = render_to_string('chat.html', {'messages': messages, 'form': form, 'chat': chat, 'user': user})
        return JsonResponse(result, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        chats = []
        for c in Chat.objects.all():
            if user in c.members.all():
                for u in c.members.all():
                    if u != user:
                        chats.append([c, u])
        context['profile'] = user
        context['chats'] = chats
        context['title'] = _('Chat')
        return context
