from django.shortcuts import render, get_object_or_404, reverse,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from render_block import render_block_to_string
import time
# Create your views here.

def index(request):
    return render(request, 'index.html')

def load_opinions(request):
    posts = Post.objects.filter(sup_post=None).order_by('-pub_date')
    context={
        'posts': posts,
    }
    html = render_block_to_string('index.html', 'opinions', context, request)
    return HttpResponse(html)

def get_post(request, post_pk):
    post = Post.objects.filter(id=post_pk).first()
    context = {
        'post': post
    }
    return render(request, 'post.html', context)


def load_sub_post(request, post_pk):
    current_user = User.objects.get(username=request.user.username)
    list_sub_posts = Post.objects.filter(sup_post=post_pk)
    sub_posts = [temp for temp in list_sub_posts if current_user in temp.user.following.all() and temp.user in current_user.following.all()]
    
    context={
        'sub_posts': sub_posts[:2]
    }
    #return render(request, 'partials/sub_post.html', context)
    html = render_block_to_string('partials/sub_post.html', 'sub_post_block', context, request)
    return HttpResponse(html)

def get_user_profile(request, username):
    user = User.objects.get(username=username)
    context={
        'target_user': user
    }
    return render(request, 'user/profile.html', context)


def toggle_follow(request, target_user):
    target_user = User.objects.get(username=target_user)
    current_user = User.objects.get(username=request.user.username)

    target_user_followers = target_user.following.all()
    print('toggling follow')

    if current_user.username != target_user.username:
        if current_user in target_user_followers:
            target_user.following.remove(current_user.id)
            print('unfollowed')
        else:
            target_user.following.add(current_user.id)
            print('followed')
    context = {
        'target_user': target_user,
    }

    return render(request, 'partials/follow_area.html', context)

def toggle_like(request, post_pk):
    current_user = get_object_or_404(User, username=request.user.username)
    post = get_object_or_404(Post, pk=post_pk)

    if current_user in post.likes.all():
        post.likes.remove(current_user)
        print('unlike')
    else:
        post.likes.add(current_user)
        print('liked')
    post.save()
    context ={
        'post': post
    }
    return render(request, 'partials/like_area.html', context)

def toggle_sub_post_like(request, post_pk):
    current_user = get_object_or_404(User, username=request.user.username)
    sub_post = get_object_or_404(Post, pk=post_pk)

    if current_user in sub_post.likes.all():
        sub_post.likes.remove(current_user)
        print('unlike')
    else:
        sub_post.likes.add(current_user)
        print('liked')
    sub_post.save()
    context ={
        'sub_post': sub_post
    }
    return render(request, 'partials/sub_post_like_area.html', context)

def toggle_sup_post_like(request, post_pk):
    current_user = get_object_or_404(User, username=request.user.username)
    post = get_object_or_404(Post, pk=post_pk)

    if current_user in post.sup_post.likes.all():
        post.sup_post.likes.remove(current_user)
        print('unlike')
    else:
        post.sup_post.likes.add(current_user)
        print('liked')
    post.sup_post.save()
    context ={
        'post': post
    }
    return render(request, 'partials/sup_post_like_area.html', context)

def share_opinion(request):
    opinion = request.POST.get('opinion')
    sup_post_id = request.POST.get('sup_post')
    from_sup_post_form = bool(request.POST.get('sup_post_form'))
    from_main_post_form = bool(request.POST.get('main_post_form'))
    from_index = bool(request.POST.get('from_index'))

    if sup_post_id is not None:
        sup_post = Post.objects.get(pk=int(sup_post_id))
    user = User.objects.filter(username=request.user.username).first()
    post = Post()
    post.user = user
    post.opinion = opinion
    if sup_post_id is not None:
        post.sup_post = sup_post
    post.save()
    posts = Post.objects.all().order_by('-pub_date')
    context={
        'posts': posts,
    }

    if from_index:
        print("from index")
        context.update({'post_status': True})
        html = render_block_to_string('index.html', 'status_block', context)
        return HttpResponse(html)

    if from_sup_post_form:
        print("from sup post")
        context.update({'post_status': True})
        html = render_block_to_string('post.html', 'status_block', context)
        return HttpResponse(html)
    
    if from_main_post_form:
        context = {
            'post_status': True,
            'post': sup_post
        }
        html = render_block_to_string('post.html', 'sub_posts_block', context)
        return HttpResponse(html)
    
    html = render_block_to_string('index.html', 'opinions', context)
    return HttpResponse(html)
    
