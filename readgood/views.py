from django.shortcuts import render
from django.views.generic import ListView, DetailView

from readgood.models import Book


# Create your views here.
def index(request):
    return render(request, 'index.html')


class BookList(ListView):
    template_name = 'readgood/book_list.html'
    queryset = Book.objects.all().order_by('title')
    paginate_by = 25


class BookDetail(DetailView):
    model = Book


class AuthorList(ListView):
    template_name = 'readgood/author_list.html'
    queryset = Book.objects.values('author')
    paginate_by = 25


class PublisherList(ListView):
    template_name = 'readgood/publisher_list.html'
    queryset = Book.objects.values('publisher')
    paginate_by = 25
