from django.contrib import admin
from .models import Post, Ekstrakurikuler, Profile

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Ekstrakurikuler)
class EkstrakurikulerAdmin(admin.ModelAdmin):
    list_display = ('name', 'instagram', 'facebook', 'youtube', 'tiktok', 'twitter')
    search_fields = ('name',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'telepon', 'alamat', 'kode_pos', 'instagram')
    search_fields = ('email', 'alamat', 'telepon')
    list_filter = ('kode_pos',)
    ordering = ('email',)