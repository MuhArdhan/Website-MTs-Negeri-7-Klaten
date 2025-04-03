from django.urls import path
from . import views

app_name = 'post'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail, name='detail'),
    path('options/', views.filter_option, name='filter_option'),
    path('filter_posts/', views.filter_posts, name='filter_posts'),
    path('create/', views.post_create, name='post_create'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/update/', views.post_update, name='post_update'),
]