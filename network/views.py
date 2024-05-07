from datetime import datetime
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import PostForm
from .models import Post, User


def index(request):
    p = Paginator(Post.objects.all().order_by("timestamp").reverse(), 10)
    page = p.page(request.GET.get("page", 1))
    return render(request, "network/index.html", {
        "form": PostForm(),
        "page": page,
        "page_range": p.page_range,
        "posts": [(post, request.user.liked_posts.filter(pk=post.id).count() if request.user.is_authenticated else 0) for post in page.object_list]
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    

def profile(request, id):
    # Get requested profile
    profile = User.objects.get(pk=id)

    # Check if the requested user is being followed by the current user
    if request.user.is_authenticated:
        is_following = request.user.following.filter(pk=id).count() > 0

    else:
        is_following = False

    p = Paginator(profile.posts.all().order_by("timestamp").reverse(), 10)
    page = p.page(request.GET.get("page", 1))
    return render(request, "network/profile.html", {
        "profile": profile,
        "page": page,
        "page_range": p.page_range,
        "posts": [(post, request.user.liked_posts.filter(pk=post.id).count() if request.user.is_authenticated else 0) for post in page.object_list],
        "is_following": is_following
    })


@login_required(login_url="/login")
def following(request):
    p = Paginator(Post.objects.filter(user__in=request.user.following.all()).order_by("timestamp").reverse(), 10)
    page = p.page(request.GET.get("page", 1))
    return render(request, "network/following.html", {
        "page": page,
        "page_range": p.page_range,
        "posts": [(post, request.user.liked_posts.filter(pk=post.id).count() if request.user.is_authenticated else 0) for post in page.object_list]
    })


@csrf_exempt
@login_required(login_url="/login")
def follow_user(request):
    # Handle posted data
    if request.method == "POST":
        # Follow the given user
        try:
            data = json.loads(request.body)
            profile = User.objects.get(pk=data["id"])
            request.user.following.add(profile)
            return JsonResponse({"error": 0, "follower_count": profile.followers.all().count()})
        
        except Exception:
            return JsonResponse({"error": 2})
        
    return JsonResponse({"error": 1})


@csrf_exempt
@login_required(login_url="/login")
def unfollow_user(request):
    # Handle posted data
    if request.method == "POST":
        # Unfollow the given user
        try:
            data = json.loads(request.body)
            profile = User.objects.get(pk=data["id"])
            request.user.following.remove(profile)
            return JsonResponse({"error": 0, "follower_count": profile.followers.all().count()})
        
        except Exception:
            return JsonResponse({"error": 2})
        
    return JsonResponse({"error": 1})
    

def new_post(request):
    # Handle posted data
    if request.method == "POST":
        # Validate form data
        form = PostForm(request.POST)

        if form.is_valid():
            # Create new post
            post = Post(
                user=request.user,
                content=form.cleaned_data["content"],
                timestamp=datetime.now()
            )
            post.save()

    # Redirect to homepage
    return HttpResponseRedirect(reverse("index"))


@csrf_exempt
@login_required
def edit_post(request):
    # Handle posted data
    if request.method == "POST":
        # Ensure that the user trying to edit this post is the owner of said post
        try:
            data = json.loads(request.body)
            post = Post.objects.get(pk=data["id"])

            if post.user != request.user:
                return JsonResponse({"error": 3})
            
        except Exception:
            return JsonResponse({"error": 2})
        
        # Update the post content
        print("New post content:")
        print(data["content"])
        post.content = data["content"]
        post.save()
        return JsonResponse({"error": 0})
    
    return JsonResponse({"error": 1})


@csrf_exempt
@login_required(login_url="/login")
def like_post(request):
    # Handle posted data
    if request.method == "POST":
        # Like the post
        try:
            data = json.loads(request.body)
            post = Post.objects.get(pk=data["id"])
            request.user.liked_posts.add(post)
            return JsonResponse({"error": 0, "likes": post.likes.all().count()})

        except Exception:
            return JsonResponse({"error": 2})

    return JsonResponse({"error": 1})


@csrf_exempt
@login_required(login_url="/login")
def unlike_post(request):
    # Handle posted data
    if request.method == "POST":
        # Like the post
        try:
            data = json.loads(request.body)
            post = Post.objects.get(pk=data["id"])
            request.user.liked_posts.remove(post)
            return JsonResponse({"error": 0, "likes": post.likes.all().count()})

        except Exception:
            return JsonResponse({"error": 2})

    return JsonResponse({"error": 1})
