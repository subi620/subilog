from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostFrom

# Create your views here.

def post_list(request):
    posts =Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})
def post_detail(request, pk):
    post =get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=pk)
    if request.method == "POST":
        comment = Comment()
        comment.post = post
        comment.body = request.POST['body']
        comment.date = timezone.now()
        comment.save()

    return render(request, 'blog/post_detail.html', {'post':post, 'comments':comments} )

def post_new(request):
    if request.method=="POST":
        form=PostFrom(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date=timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostFrom()
    return render(request, 'blog/post_edit.html', {'form':form})

def post_edit(request, pk):
    post=get_object_or_404(Post, pk=pk)

    if request.method =="POST":
        form = PostFrom(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_detail', pk=post.pk)


    else:
        form = PostFrom(instance=post)

    return render(request, 'blog/post_edit.html', {'form':form})
