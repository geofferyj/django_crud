from crud_app.forms import PostForm, UserRegisterForm
from crud_app.models import CRUDPost
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.http.request import HttpRequest
# Create your views here.

def home(request):
    posts = CRUDPost.objects.all()
    return render(request, "crud_app/home.html", {"posts":posts})


def get_post(request, post_id):
    post = get_object_or_404(CRUDPost, id=post_id)

    return render(request, "crud_app/post_detail.html", {"post":post})


def add_post(request: HttpRequest):

    if request.method == 'POST':
        user = request.user
        form = PostForm(request.POST)
        if form.is_valid():
            # Create Post object but don't save to database yet
            new_post: CRUDPost = form.save(commit=False)
            # Assign the current post to the comment
            new_post.post_author = user           
            new_post.save()
            return redirect("home")
    else:
        form = PostForm()

    return render(request, "crud_app/add_post.html", {'form': form})


def update_post(request: HttpRequest, post_id):

    post = get_object_or_404(CRUDPost, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()          
            return redirect("home")
    else:
        form = PostForm(instance=post)

    return render(request, "crud_app/add_post.html", {'form': form})

def delete_post(request, post_id):
    post = get_object_or_404(CRUDPost, id=post_id)
    post.delete()
    return redirect("home")


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()          
            return redirect('home')
    
    form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})
