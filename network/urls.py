
from django.urls import path

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allposts/", views.allposts, name="allposts"),
    path("postcomment", views.postcomment, name = "postcomment"),
    path("likeposts/<int:id>", views.addlikes, name="addlike"),
    path("myposts", views.posts, name="myposts"),
    path("next", views.next, name = "next"),
    path("edit/<int:id>", views.edit, name = "edit"),
    path("submit/<int:id>", views.submit, name = "submit")
]
