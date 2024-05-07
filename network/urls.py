
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("profile/following", views.following, name="following"),
    path("profile/follow", views.follow_user, name="follow"),
    path("profile/unfollow", views.unfollow_user, name="unfollow"),
    path("new-post", views.new_post, name="new-post"),
    path("edit-post", views.edit_post, name="edit-post"),
    path("like-post", views.like_post, name="like-post"),
    path("unlike-post", views.unlike_post, name="unlike-post")
]
