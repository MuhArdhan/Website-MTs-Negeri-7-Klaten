from django.shortcuts import render
from .models import Post, Ekstrakurikuler, Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    post = Post.objects.all()
    ekstrakurikuler = Ekstrakurikuler.objects.all()
    profile = Profile.objects.first()
    prestasi_posts = Post.published.filter(category=Post.Category.PRESTASI)
    paginator = Paginator(post, 4)
    page_number = request.GET.get('page', 1)
    post = paginator.page(page_number)
    return render(request, 'index.html' , {'post': post, 'ekstrakurikuler': ekstrakurikuler, 'profile': profile, 'prestasi_posts': prestasi_posts})
