from django.shortcuts import render
from django.views.generic import ListView, DetailView

from readgood.models import Book, Author, Publisher


# Create your views here.
def index(request):
    return render(request, 'index.html')


class BookList(ListView):
    template_name = 'readgood/book_list.html'
    paginate_by = 25
    model = Book


class BookDetail(DetailView):
    model = Book


class AuthorList(ListView):
    template_name = 'readgood/author_list.html'
    model = Author
    paginate_by = 25


class AuthorDetail(DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(**kwargs)
        context['book_list'] = self.object.book_set.all()
        return context


class PublisherList(ListView):
    template_name = 'readgood/publisher_list.html'
    model = Publisher
    paginate_by = 25


class PublisherDetail(DetailView):
    model = Publisher

    def get_context_data(self, **kwargs):
        context = super(PublisherDetail, self).get_context_data(**kwargs)
        context['book_list'] = self.object.book_set.all()
        return context
