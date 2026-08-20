# Create your views here.
from django.shortcuts import render, redirect
from book.models import Book
from author.models import Author
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404

@login_required
def book_detail(request, book_id):
    book = Book.get_by_id(book_id)
    if book is None:
        raise Http404("Not found")
    return render(request, 'book/book_detail.html', {'book': book})

@login_required
@permission_required('is_staff', raise_exception=True)
def create_a_book(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        count = request.POST.get('count')
        author_ids = request.POST.getlist('authors')
 
        book = Book.create(name, description, count)
 
        if author_ids:
            authors = Author.objects.filter(id__in=author_ids)
            book.add_authors(authors)
 
        return redirect('book_detail', book_id=book.id)
 
    authors = Author.objects.all()
    return render(request, 'book/create_a_book.html', {'authors': authors})

@login_required
def list_of_books(request):
    books = Book.objects.all()
    name = request.GET.get('name')
    author = request.GET.get('author')

    if name:
        books = books.filter(name__icontains=name)
    if author:
        books = books.filter(authors__surname__icontains=author)

    return render(request, 'book/list_of_books.html', {'books': books})

@login_required
@permission_required('is_staff', raise_exception=True)
def ordered_books_by_user(request, user_id):
    return redirect(f"/orders/?user={user_id}")