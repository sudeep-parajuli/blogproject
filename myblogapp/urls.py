from django.urls import path
from myblogapp import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("post/(?P<pk>\d+)/", views.PostDeleteView.as_view(), name="post_detail"),
    path("post/new/", views.CreatePostView.as_view(), name="new_post"),
    path("post/(?P<pk>\d+)/edit/", views.PostUpdateView.as_view(), name="post_detail"),
    path("drafts/", views.DraftListView.as_view(), name="post_draft_list"),
    path("post/(?P<pk>\d+)/remove/", views.PostDeleteView.as_view(), name="remove_post"),
    
]