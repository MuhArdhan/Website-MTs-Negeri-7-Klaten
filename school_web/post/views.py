from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required  # Tambahkan login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.utils.dateparse import parse_date
from django.db.models import Count
from django.http import JsonResponse
from home.models import Post
from home import urls
from django.urls import reverse
from django.db.models import Q
from .forms import PostForm

# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    recent_posts = Post.objects.order_by('-publish')[:5] 
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
    
    context = {
        'posts': posts,
        'recent_posts': recent_posts
    }

    return render(request, 'post/post_display.html' , context)

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug, publish__year=year, publish__month=month, publish__day=day)

    return render(request, 'post/detail.html', {
        'post': post,
    })



def filter_option(request):
    filter_type = request.GET.get('type')
    data = {'options': []}

    if filter_type == 'category':
        categories = Post.Category.choices
        data['options'] = [{'value': cat[0], 'text': cat[1]} 
                           for cat in categories]
    elif filter_type == 'author':
        User = get_user_model()
        authors = User.objects.filter(blog_posts__isnull=False).distinct()  # Hanya ambil author yang memiliki post
        data['options'] = [{'value': author.id, 'text': author.username} 
                           for author in authors]
    elif filter_type == 'tag':
        tags = []
        for post in Post.objects.all():
            tags.append(post.tags.all())
        print(tags)
        data['options'] = [{'value': tag.id, 'text': tag.name} 
                           for tag in Post.tags.all()]
    
    return JsonResponse(data)

def filter_posts(request):
    # Get filter criteria from the request
    filter_by = request.GET.get('filter_by')  # "category", "tag", "author", etc.
    filter_value = request.GET.get('filter_value')  # The value to filter by
    start_date = request.GET.get('start_date')  # Start date for filtering
    end_date = request.GET.get('end_date')  # End date for filtering
    sort_by = request.GET.get('sort_by')  # Value to sort by
    search_title = request.GET.get('search_title')

    # Filter session
    if filter_by == 'category' and filter_value:
        posts = Post.objects.filter(category=filter_value)
    elif filter_by == 'tag' and filter_value:
        posts = Post.objects.filter(tags=filter_value)
    elif filter_by == 'author' and filter_value:
        posts = Post.objects.filter(author=filter_value)
    elif filter_by == 'date' and (start_date or end_date):
        # Jika start_date atau end_date ada, lakukan filter berdasarkan range
        if start_date or end_date:
            start_date = parse_date(start_date) if start_date else None
            end_date = parse_date(end_date) if end_date else None

            # Filter berdasarkan rentang tanggal
            if start_date and end_date:
                posts = Post.objects.filter(publish__date__range=[start_date, end_date])
            elif start_date:
                posts = Post.objects.filter(publish__date__gte=start_date)
            elif end_date:
                posts = Post.objects.filter(publish__date__lte=end_date)
        else:
            posts = Post.objects.none()
    else:
        posts = Post.objects.all()  # Default case, if no filter is applied

 
    # Annotate post with comment count
    posts = posts.annotate(comment_count=Count('comments'))

    # Filter by search title
    if search_title:
        posts = posts.filter(title__icontains=search_title)


    # Tambahkan sorting
    if sort_by == 'date_asc':
        posts = posts.order_by('publish')
    elif sort_by == 'date_desc':
        posts = posts.order_by('-publish')
    elif sort_by == 'comment_asc':
        posts = posts.order_by('comment_count')
    elif sort_by == 'comment_desc':
        posts = posts.order_by('-comment_count')
    elif sort_by == 'title_asc':
        posts = posts.order_by('title')
    elif sort_by == 'title_desc':
        posts = posts.order_by('-title')


    
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)

    # Create a JSON response
    post_data = []
    for post in posts:
        post_data.append({
            'title': post.title,
            'author': post.author.username,
            'category': post.category,
            'publish_date': post.publish.strftime('%Y-%m-%d'),
            'excerpt': post.body, 
            'image_url': post.image.url if post.image else '',
            'tags': [tag.name for tag in post.tags.all()],
            'detail_url': post.get_absolute_url(),
        })


    return JsonResponse({'posts': post_data})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Explicitly set the author to logged-in user
            post.save()  
            
            form.save_m2m()  
            
            return redirect('post:detail', post.publish.year, post.publish.month, post.publish.day, post.slug)  # Alihkan ke halaman detail post
    else:
        form = PostForm()

    return render(request, 'post/create/post_create.html', {'form': form})

@login_required
def post_delete(request, slug, year, month, day):
    post = get_object_or_404(Post, slug=slug, publish__year=year, publish__month=month, publish__day=day)
    
    # Hanya penulis atau admin yang bisa menghapus
    if request.user == post.author or request.user.is_superuser:
        post.delete()
        return redirect('home:home')  # Redirect ke halaman home setelah menghapus
    else:
        return redirect(post.get_absolute_url())  # Jika bukan author, redirect ke detail post
    
@login_required
def post_update(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug, publish__year=year, publish__month=month, publish__day=day)
    print(post.title)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('article:detail', args=[post.publish.year, post.publish.month, post.publish.day, post.slug]))
    else:
        form = PostForm(instance=post)

    return render(request, 'post/update/post_update.html', {'form': form, 'post': post})

def search_posts(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    return render(request, 'post/article_display.html', {'results': results, 'query': query})