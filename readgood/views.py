from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from readgood.models import Book, Author, Publisher


# Create your views here.
def index(request):
    return render(request, 'index.html')


def search(request):
    #  Grab parameters
    draw = int(request.GET['draw'])
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    end = start + length

    #  As far as I can tell, I need to do this because the way DataTables sends data does not cooperate with the way
    #  Django accepts data.
    col_param = 'columns[' + request.GET['order[0][column]'] + '][data]'
    ord_column = request.GET[col_param]
    search_key = request.GET["search[value]"]

    books = Book.objects.all().order_by(ord_column)
    if search_key:
        books = books.filter(Q(title__icontains=search_key)
                             | Q(author__name__icontains=search_key)
                             | Q(publisher__name__icontains=search_key))
    data = books[start:end]
    total = books.count()

    response = {
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,
        #  TODO: remove values, make generic. Might mean handling dicts
        'data': list(data.values('title', 'author', 'publisher'))
    }

    return JsonResponse(response)


class BookList(ListView):
    template_name = 'readgood/book_list.html'
    paginate_by = 25
    model = Book

    # TODO: self.request.GET.get('publisher')


class BookDetail(DetailView):
    model = Book


class AuthorList(ListView):
    template_name = 'readgood/author_list.html'
    model = Author
    paginate_by = 25

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


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
