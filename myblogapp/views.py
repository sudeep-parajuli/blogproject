from django.shortcuts import render, get_object_or_404, redirect
from myblogapp.models import Post, Comment
from django.utils import timezone
from myblogapp.forms import PostForm, CommentForm
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
class AboutView(TemplateView):
    template_name = "about.html"

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by("-published_date")

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    redirect_field_name = "myblogapp/post_detail.html"

    form_class = PostForm
    model =Post

class DraftListView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "myblogapp/post_draft_list.html"
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by("-published_date")


class PostUpdateView(UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')



#######################################
## Functions that require a pk match ##
#######################################

@login_required
def post_publish(request, pkk):
    post = get_object_or_404(Post, pk=pkk)
    post.published()
    return redirect("post_detail", pk=pkk)


@login_required
def add_comment_to_post(request, pkk):
    post = get_object_or_404(Post, pk=pkk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect("post_detail", pk=post.pkk)
    else:
        form = CommentForm()
    return render(request, "my_blog/comment_form.html", {"form":form})


@login_required
def comment_approve(request, pkk):
    comment = get_object_or_404(Comment, pk = pkk)
    comment.approved()
    return redirect("post_detail", pk=comment.post.pkk)


@login_required
def comment_remove(request, pkk):
    comment = get_object_or_404(Comment, pk= pkk)
    post_pk = comment.post.pkk
    comment.delete()
    return redirect ("post_detail", pk=post_pk)    

