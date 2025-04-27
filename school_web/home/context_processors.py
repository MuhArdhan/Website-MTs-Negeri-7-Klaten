from .models import Profile, Post

def footer_data(request):
    profile = Profile.objects.first()
    info_posts = Post.published.filter(category=Post.Category.INFO)
    return {
        'profile': profile,
        'info_posts': info_posts,
    }