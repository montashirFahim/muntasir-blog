from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('signup/', views.signUp, name='signup'),
    path('login/', views.login, name='login'),
    path('blog/', views.blogs, name='blog_list'),
    path('categories/', views.Categories, name='category_list'),
    path('profile/', views.profile, name='profile'),
    path('write-blog/', views.BlogWrite, name='blog_write'),
    path('notifications/', views.Notifications, name='notifications'),
    path('pending-blogs/', views.PendingBlogs, name='pending_blogs'),
    path('logout/', views.logout_view, name='logout'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('delete-blog/<int:blog_id>/', views.DeleteBlog, name='delete_blog'),
]
