from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import *
from .forms import *

# Create your views here.
def Home(request):
    return render(request, 'index.html')

def signUp(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

def blogs(request):
    all_blogs = Blog.objects.filter(is_approved=True).order_by('-views', '-created_at')
    
    paginator = Paginator(all_blogs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blogs.html', {'page_obj': page_obj})


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    # increment views
    blog.views += 1
    blog.save()

    comments = Comment.objects.filter(blog=blog, parent=None).order_by('-created_at')

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get("parent_id")

            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.blog = blog

            # handle reply
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                new_comment.parent = parent_comment

            new_comment.save()

            # Notify blog author when someone comments
            if new_comment.parent is None:
                if blog.author != request.user:
                    Notification.objects.create(
                        user=blog.author,
                        message=f"{request.user.username} commented on your blog '{blog.title}'."
                    )

            # Notify comment owner when someone replies
            else:
                parent_comment = new_comment.parent
                if parent_comment.user != request.user:
                    Notification.objects.create(
                        user=parent_comment.user,
                        message=f"{request.user.username} replied to your comment on '{blog.title}'."
                    )

            return redirect('blog_detail', slug=blog.slug)

    else:
        form = CommentForm()

    return render(request, "blog_detail.html", {
    "blog": blog,
    "comments": comments,
    "comment_form": CommentForm(),
    "reply_form": CommentForm(),
    })


def Categories(request):
    # Fetch all approved blogs
    blogs = Blog.objects.filter(is_approved=True)

    # Create a mapping: category_name -> list of blogs
    category_map = {}
    for blog in blogs:
        category_name = blog.category if blog.category else "Uncategorized"
        if category_name not in category_map:
            category_map[category_name] = []
        category_map[category_name].append(blog)  # append the whole blog object

    return render(request, "categories.html", {"category_map": category_map})



@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Update profile if form submitted
    if request.method == "POST":
        bio = request.POST.get("bio")
        avatar = request.FILES.get("avatar")

        profile.bio = bio
        if avatar:
            profile.avatar = avatar
        profile.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("profile")

    # Fetch user's blogs
    user_blogs = Blog.objects.filter(author=request.user).order_by('-created_at')
    paginator = Paginator(user_blogs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "profile.html", {
        "profile": profile,
        "page_obj": page_obj,
    })


@login_required
def DeleteBlog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)
    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog deleted successfully.")
        return redirect("profile")
    return render(request, "confirm_delete.html", {"blog": blog})


@login_required
def BlogWrite(request):
    blog_id = request.GET.get("edit")
    blog = None

    if blog_id:
        blog = get_object_or_404(Blog, id=blog_id, author=request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        category = request.POST.get("category")  
        content = request.POST.get("content")

        if blog:
            blog.title = title
            blog.category = category
            blog.content = content
            blog.is_approved = False
            blog.save()

            messages.success(request, "Blog updated and moved to pending review.")
        else:
            Blog.objects.create(
                author=request.user,
                title=title,
                category=category,
                content=content,
                is_approved=False,
            )
            messages.success(request, "Blog submitted for review.")

        return redirect("blog_list")

    return render(request, "write-blog.html", {
        "blog": blog,
    })

@login_required
def Notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    # Mark all unread as read
    notifications.filter(is_read=False).update(is_read=True)

    return render(request, "notifications.html", {
        "notifications": notifications
    })




@login_required
def PendingBlogs(request):
    if not request.user.is_superuser:
        return redirect("home")

    if request.method == "POST":
        blog_id = request.POST.get("blog_id")
        action = request.POST.get("action")
        blog = get_object_or_404(Blog, id=blog_id)

        if action == "approve":
            blog.is_approved = True
            blog.save()
            Notification.objects.create(user=blog.author, message=f"Your blog '{blog.title}' has been approved.")
            messages.success(request, f"Blog '{blog.title}' approved.")
        elif action == "reject":
            Notification.objects.create(
                user=blog.author,
                message=f"Your blog '{blog.title}' has been rejected."
                )
            blog.delete()
            messages.success(request, f"Blog '{blog.title}' rejected and removed.")


        return redirect("pending_blogs")

    pending_blogs = Blog.objects.filter(is_approved=False).order_by("created_at")
    return render(request, "pending-blog.html", {"pending_blogs": pending_blogs})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')
