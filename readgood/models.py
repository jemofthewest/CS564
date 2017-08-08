from django.contrib.auth.models import User
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

    class Meta:
        ordering = ["title"]


class Author(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    slug = models.SlugField(max_length=255)

    def get_absolute_url(self):
        return reverse('author_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    slug = models.SlugField(max_length=255)

    def get_absolute_url(self):
        return reverse('publisher_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    location = models.CharField(max_length=255, null=True)
    age = models.PositiveSmallIntegerField(null=True)
    favorite_book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    favorite_author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)


class Award(models.Model):
    name = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField()
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    genre = models.CharField(max_length=100)

    class Meta:
        #  Django doesn't allow for primary keys with multiple fields, so I need to allow Django to generate the
        #  automatic ID, but then require the primary key to be unique
        unique_together = (('name', 'year'),)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    RATING_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10')
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)

    class Meta:
        unique_together = (('user', 'book'),)


class BooksToRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'book'),)


class BooksRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'book'),)
