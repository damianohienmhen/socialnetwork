from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.db.models import Model
import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


from .models import User, Post
from .forms import CommentPosts, EditPosts


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "network/index.html")


def allposts(request):
    cf = CommentPosts(request.POST or None)
    return HttpResponseRedirect(reverse("next"))

def posts(request):
    # Get all the posts
    
    posts = Post.objects.all().order_by("created").all()
    return JsonResponse([post.serialize() for post in posts], safe=False) 

def next(request):
    cf = CommentPosts(request.POST or None)
    posts = Post.objects.all().order_by("created").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/allposts.html", {'page_obj': page_obj,"post_comment":cf})   


def addlikes(request, id):
    post = Post.objects.get(id = id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    post.save()
    likescount = int(post.likes.count())
    postid = int(post.id)
    list = {"likescount":likescount , "postid":postid }
   
    return JsonResponse(list, safe=False)
    

def edit(request, id):
    post = Post.objects.get(id = id)
    post_content = post.post_content
    postid = int(post.id)
    editlist = {"post_content": post_content, "postid": postid}
    
    return JsonResponse(editlist, safe=False)
    
  
def submit(request, id):
    if request.method == 'POST': 
        if request.POST.get("update"):
            post = Post.objects.get(id = id)
            postid = int(post.id)
            updatepost = request.POST.get("updatepost")
            post.post_content = str(updatepost)
            post.save(update_fields=["post_content"])
            submitlist = [{"post_content": post.post_content, "postid": post.id}]
    
        return HttpResponseRedirect(reverse("next"))

def follow(request, theuser):
    follower = User.objects.get(username = request.user)
    followers = follower.followers.all()
    persontofollow = User.objects.get(username = theuser)
    if persontofollow in followers:
        follower.followers.remove(persontofollow)
        
        theuser = User.objects.get(username = theuser)
        userposts = Post.objects.filter(user = theuser)
        paginator = Paginator(userposts, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
        return render(request, "network/profilepage.html", {"page_obj": page_obj, 
        "userposts": userposts, "theuser": theuser, "message": ("You've Succesfully Unfollowed %s " %persontofollow)})
    else:
        follower.followers.add(persontofollow)
        
        theuser = User.objects.get(username = theuser)
        userposts = Post.objects.filter(user = theuser)
        paginator = Paginator(userposts, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
        return render(request, "network/profilepage.html", {"page_obj": page_obj, 
        "userposts": userposts, "theuser": theuser, "message": ("You've Succesfully Followed %s " %persontofollow)})

def following(request):
    currentuser = User.objects.get(username = request.user)
    followingusers = currentuser.followers.all()
    followingposts = Post.objects.filter(user__id__in= followingusers)
    
    paginator = Paginator(followingposts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {"page_obj": page_obj,})   
                   
def profilepage(request, user):
    theuser = User.objects.get(username = user)
    userposts = Post.objects.filter(user = theuser)
    paginator = Paginator(userposts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/profilepage.html", {"page_obj": page_obj, "userposts": userposts, "theuser": theuser}) 

        
def postcomment(request):
    if request.method == 'POST': 
        cf = CommentPosts(request.POST or None) 
        if cf.is_valid(): 
            if request.POST.get("post"):
                post_content = request.POST.get("post_content") 
                comment = Post.objects.create(user = request.user, post_content = post_content) 
                comment.save()
            else:
                cf = CommentPosts() 
        return HttpResponseRedirect(reverse("allposts"))

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
