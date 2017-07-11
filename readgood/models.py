from django.db import models
from django.urls import reverse


# Create your models here.
class Book(models.Model):
    isbn = models.CharField(primary_key=True, max_length=13)
    title = models.CharField(blank=True, null=True, max_length=255)
    author = models.ForeignKey('Author', on_delete=models.PROTECT)
    year_published = models.IntegerField(blank=True, null=True)
    publisher = models.ForeignKey('Publisher', on_delete=models.PROTECT)
    image_url_s = models.URLField(blank=True, null=True)
    image_url_m = models.URLField(blank=True, null=True)
    image_url_l = models.URLField(blank=True, null=True)
    slug = models.SlugField(max_length=255)

    def get_absolute_url(self):
        return reverse('book_slug', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.name
