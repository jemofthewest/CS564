from django.db import models


# Create your models here.
class Book(models.Model):
    isbn = models.CharField(primary_key=True, max_length=13)
    title = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    year_published = models.IntegerField(blank=True, null=True)
    publisher = models.TextField(blank=True, null=True)
    image_url_s = models.URLField(blank=True, null=True)
    image_url_m = models.URLField(blank=True, null=True)
    image_url_l = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
