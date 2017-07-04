from django.views.generic import ListView
from readgood.models import Book


# Create your views here.
class BookList(ListView):
    template_name = 'readgood/book_list.html'
    queryset = Book.objects.all().order_by('title')
    paginate_by = 25
