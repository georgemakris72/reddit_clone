from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post
# Create your views here.

#decorator that makes view need log in before view can be accessed, otherwise it takes you back to login page.  url up top will be login url followedd by a next= which lists page you were at previously so that once you are logged in it will take you back there.
@login_required
def create(request):
    if request.method=="POST":
        if request.POST['title'] and request.POST['url']:
            post=Post()
            post.title=request.POST['title']
            # following checks to see if inputed url starts with http or https.  Needs this to be directed to correct website.  If it doesn't we need to insert it.
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                post.url=request.POST['url']
            else:
                post.url='http://'+request.POST['url']
            post.pub_date=timezone.datetime.now()
            post.author=request.user#would have had to do post.votes too but that will be taken care of in another step
            post.save()
            # return render(request, 'posts/home.html')#if just used render, it would display contents of homepage but url would still be stuck on create posts page
            return redirect('home')
        else:
            return render(request, 'posts/create.html', {'error':'ERROR: You must include a title and a url to create a post'})

    else:
        return render(request, 'posts/create.html')

def home(request):
    posts=Post.objects.order_by('-votes_total')
    return render(request, 'posts/home.html', {'posts':posts})

def userposts(request):
    posts=Post.objects.filter(author=request.author.id).order_by('-votes_total')
    return render(request, 'posts/home.html', {'posts':posts})



def upvote(request,pk):
    if request.method=="POST":
        post=Post.objects.get(pk=pk)
        post.votes_total += 1
        post.save()
        return redirect('home')

def downvote(request,pk):
    if request.method=="POST":
        post=Post.objects.get(pk=pk)
        post.votes_total -= 1
        post.save()
        return redirect('home')
