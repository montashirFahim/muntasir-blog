from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('signup/', views.signUp, name='signup'),
    path('login/', views.login, name='login'),
    path('blog/', views.blogs, name='blog_list'),
    path('categories/', views.Categories, name='category_list'),
    path('profile/', views.Profile, name='profile'),
    path('write-blog/', views.BlogWrite, name='blog_write'),
    path('notifications/', views.Notifications, name='notifications'),
    path('pending-blogs/', views.PendingBlogs, name='pending_blogs'),
    path('logout/', views.logout, name='logout'),
]
