from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
]