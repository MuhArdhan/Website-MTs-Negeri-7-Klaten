from django.shortcuts import render
from .models import Post

def index(request):
    post = Post.objects.all()
    return render(request, 'index.html' , {'post': post})
