from django.urls import path

from Creffeny import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('registration/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('post/<int:pk>/', views.PostView.as_view(), name='post'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]