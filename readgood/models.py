from django.db import models


# Create your models here.
class Book(models.Model):
    isbn = models.CharField(primary_key=True, max_length=13)
    title = models.CharField(blank=True, null=True, max_length=255)
    author = models.CharField(blank=True, null=True, max_length=255)
    year_published = models.IntegerField(blank=True, null=True)
    publisher = models.CharField(blank=True, null=True, max_length=255)
    image_url_s = models.URLField(blank=True, null=True)
    image_url_m = models.URLField(blank=True, null=True)
    image_url_l = models.URLField(blank=True, null=True)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    slug = models.SlugField(max_length=255)


class Publisher(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    slug = models.SlugField(max_length=255)
