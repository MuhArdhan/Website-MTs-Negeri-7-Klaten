from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import KotakSaranForm
from .models import Post, Ekstrakurikuler, Profile, TenagaPendidik
from django.core.paginator import Paginator

def index(request):
    post = Post.objects.all()
    ekstrakurikuler = Ekstrakurikuler.objects.all()
    profile = Profile.objects.first()
    prestasi_posts = Post.published.filter(category=Post.Category.PRESTASI)
    info_posts = Post.published.filter(category=Post.Category.INFO)
    tendik = TenagaPendidik.objects.all()
    paginator_post = Paginator(post, 4)
    page_number = request.GET.get('page', 1)
    post = paginator_post.page(page_number)
    form = KotakSaranForm()

    # cek success dari GET parameter
    success = request.GET.get('success') == '1'

    if request.method == 'POST':
        form = KotakSaranForm(request.POST)
        if form.is_valid():
            saran = form.save()

            # Kirim email ke admin
            subject = f"Saran Baru dari {saran.nama}"
            message = f"""
                        Nama: {saran.nama}
                        Email: {saran.email}
                        Telepon: {saran.telepon}

                        Pesan:
                        {saran.pesan}
                        """
            admin_email = settings.ADMIN_EMAIL
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email])

            return redirect('/?success=1#kotak-saran')  # <-- redirect membawa success=1

    context = {
        'form': form,
        'success': success,
        'post': post,
        'ekstrakurikuler': ekstrakurikuler,
        'profile': profile,
        'prestasi_posts': prestasi_posts,
        'tendik': tendik,
        'info_posts': info_posts
    }
    return render(request, 'index.html', context)

def all_posts(request):
    category = request.GET.get('category')  # Ambil kategori dari URL
    search_query = request.GET.get('search')  # Ambil pencarian dari URL
    
    posts = Post.objects.all()  # Ambil semua data awal
    if category:  # Filter berdasarkan kategori jika ada
        posts = posts.filter(category=category)
    if search_query:  # Filter berdasarkan pencarian jika ada
        posts = posts.filter(title__icontains=search_query)  # Cari judul yang mengandung kata
    
    categories = Post.objects.values_list('category', flat=True).distinct()  # Ambil semua kategori unik
    return render(request, 'post/all_posts.html', {
        'posts': posts,
        'categories': categories,
        'selected_category': category,
        'search_query': search_query,
    })
