from django.shortcuts import render
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    post = Post.objects.all()
    paginator = Paginator(post, 4)
    page_number = request.GET.get('page', 1)
    post = paginator.page(page_number)
    return render(request, 'index.html' , {'post': post})
