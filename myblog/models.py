# from django.db import models
# from django.contrib.auth.models import User
# from django.utils.text import slugify
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     total_blog_views = models.IntegerField(default=0)
#     bio = models.TextField(blank=True)
#     avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

#     def __str__(self):
#         return f'{self.user.username} Profile'

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# class Category(models.Model):
#     name = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return self.name

# class Blog(models.Model):
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
#     title = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True, blank=True)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='blogs')
#     views = models.IntegerField(default=0)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_approved = models.BooleanField(default=False)

#     def __str__(self):
#         return self.title

# class Notification(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
#     message = models.CharField(max_length=200)
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Notification for {self.user.username}: {self.message}"

# class Comment(models.Model):
#     blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
#     content = models.TextField()
#     is_approved = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['created_at']

#     def __str__(self):
#         return f"Comment by {self.user.username} on {self.blog.title}"

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_blog_views = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=100)
    views = models.IntegerField(default=0)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-views', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=200)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.title}"
