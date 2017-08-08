from django.db.models import Avg, Q, Count
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from readgood.forms import AddBookForm
from readgood.models import *


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

    books = Book.objects.all()
    books = books.order_by(ord_column)
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
        'data': list(data.values('isbn', 'title', 'author', 'publisher'))
    }

    return JsonResponse(response)


class BookList(ListView):
    template_name = 'readgood/book_list.html'
    paginate_by = 25
    model = Book


class BookDetail(View):
    def get(self, request, *args, **kwargs):
        view = BookDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AddBook.as_view()
        return view(request, *args, **kwargs)


# Override get_object?
class BookDisplay(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super(BookDisplay, self).get_context_data(**kwargs)
        context['form'] = AddBookForm()
        context['read'] = self.object.booksread_set.filter(user_id=self.request.user.id).exists()
        context['to_read'] = self.object.bookstoread_set.filter(user_id=self.request.user.id).exists()
        context['avg_rating'] = self.object.rating_set.aggregate(Avg('rating'))['rating__avg']
        return context


class AddBook(SingleObjectMixin, FormView):
    template_name = 'readgood/book_detail.html'
    form_class = AddBookForm
    model = Book
    success_message = "Book added successfully"

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super(AddBook, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        isbn = self.object.isbn
        user_id = self.request.user.id
        toread = self.object.bookstoread_set.filter(book_id=isbn, user_id=user_id)
        read = self.object.booksread_set.filter(book_id=isbn, user_id=user_id)

        book_list = form.data.get('book_list')
        if book_list == 'read':
            (b, _) = BooksRead.objects.get_or_create(book_id=isbn, user_id=user_id)
            b.save()
            if toread.exists():
                toread.delete()
        elif book_list == 'to-read':
            (b, _) = BooksToRead.objects.get_or_create(book_id=isbn, user_id=user_id)
            b.save()
            if read.exists():
                read.delete()
        else:
            if toread.exists():
                toread.delete()
            if read.exists():
                read.delete()

        if 'favorite' in form.data:
            (p, _) = Profile.objects.get_or_create(user_id=user_id)
            p.favorite_book_id = isbn
            p.save()

        rating = form.data.get('rating')

        if rating:
            r = Rating.objects.filter(book_id=isbn, user_id=user_id)
            if r.exists():
                r.update(rating=rating)
                r[0].save()
            else:
                r = Rating(book_id=isbn, user_id=user_id, rating=rating)
                r.save()

        return super(AddBook, self).form_valid(form)

    def get_success_url(self):
        return reverse('book_pk', kwargs={'pk': self.object.pk})


class AuthorList(ListView):
    template_name = 'readgood/author_list.html'
    model = Author
    paginate_by = 25

    def get_queryset(self):
        qset = super(AuthorList, self).get_queryset().annotate(num_books=Count('book'),
                                                               avg_rating=Avg('book__rating__rating'))
        return qset


class AuthorDetail(DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(**kwargs)
        booklist = self.object.book_set
        context['book_list'] = booklist.all()
        context['avg_rating'] = booklist.aggregate(Avg('rating__rating'))['rating__rating__avg']
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


class UserDetail(DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        context['to_read'] = self.object.bookstoread_set.all()
        context['read'] = self.object.booksread_set.all()
        context['ratings'] = self.object.rating_set.all()

        recommended_books = Book.objects.raw('select readgood_book.isbn from readgood_rating '
                                             'inner join readgood_book on readgood_rating.book_id = readgood_book.isbn '
                                             'where user_id in '
                                             '(select other_users.user_id from '
                                             '(select book_id from readgood_rating '
                                             'where user_id = %s and rating = 10) as favorite_books '
                                             'inner join readgood_rating as other_users on favorite_books.book_id = other_users.book_id '
                                             'where other_users.rating = 10 and other_users.user_id <> %s) '
                                             'and rating = 10 '
                                             'and book_id not in '
                                             '(select book_id from readgood_rating '
                                             'where user_id = %s) '
                                             'group by book_id '
                                             'ORDER BY count(*) desc '
                                             'LIMIT 10' % (self.object.id, self.object.id, self.object.id))
        context['recommend'] = recommended_books
        return context
