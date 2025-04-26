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
    tendik = TenagaPendidik.objects.all()
    paginator = Paginator(post, 4)
    page_number = request.GET.get('page', 1)
    post = paginator.page(page_number)
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
    }
    return render(request, 'index.html', context)