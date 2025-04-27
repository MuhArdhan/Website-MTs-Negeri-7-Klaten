from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'home'

urlpatterns = [
    path('', views.index , name='home'),
    path('all-posts/', views.all_posts, name='all_posts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)