from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import *

# Create your views here.
def Home(request):
    return render(request, 'index.html')

def signUp(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Profile is automatically created via post_save signal
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
    
    # Pagination: 10 blogs per page
    paginator = Paginator(all_blogs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blogs.html', {'page_obj': page_obj})

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_approved=True)
    
    blog.views += 1
    blog.save(update_fields=['views'])
    
    return render(request, 'blog_detail.html', {'blog': blog})

def Categories(requeust):
    pass

def Profile(request):
    pass

@login_required
def BlogWrite(request):
    blog_id = request.GET.get("edit")
    blog = None

    if blog_id:
        blog = get_object_or_404(Blog, id=blog_id, author=request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        category = request.POST.get("category")   # now a string
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
                category=category,   # stored as string
                content=content,
                is_approved=False,
            )
            messages.success(request, "Blog submitted for review.")

        return redirect("blog_list")

    return render(request, "write-blog.html", {
        "blog": blog,
    })


def Notifications(request):
    pass


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
            # Notify author
            Notification.objects.create(user=blog.author, message=f"Your blog '{blog.title}' has been approved.")
            messages.success(request, f"Blog '{blog.title}' approved.")
        elif action == "reject":
            blog.delete()
            messages.success(request, f"Blog '{blog.title}' rejected and removed.")

        return redirect("pending_blogs")

    pending_blogs = Blog.objects.filter(is_approved=False).order_by("created_at")
    return render(request, "pending-blog.html", {"pending_blogs": pending_blogs})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')
