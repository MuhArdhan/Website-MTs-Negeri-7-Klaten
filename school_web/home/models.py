from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    class Category(models.TextChoices):
        AGENDA = 'Agenda', 'Agenda'
        INFO = 'Info', 'Info'
        BERITA = 'Berita', 'Berita'
        PRESTASI = 'Prestasi', 'Prestasi'

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )
    category = models.CharField(
        max_length=10,
        choices=Category,
        default=Category.AGENDA
    )

    image = models.ImageField(upload_to='blog/',  default='blog/default.jpg')

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'post:detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ],
        )
    
class Ekstrakurikuler(models.Model):
    name = models.CharField(max_length=250)
    deskripsi = models.TextField()
    instagram = models.CharField(max_length=250)
    facebook = models.CharField(max_length=250)
    youtube = models.CharField(max_length=250)
    tiktok = models.CharField(max_length=250)
    twitter = models.CharField(max_length=250)
    image = models.ImageField(upload_to='ekstrakurikuler/', default='ekstrakurikuler/default.jpg')