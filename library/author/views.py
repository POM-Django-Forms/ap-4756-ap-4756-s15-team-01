from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from author.models import Author

app_name = 'author'

@login_required
@permission_required('is_staff', raise_exception=True)
def list_of_authors(request):
    authors = Author.objects.all()
    name = request.GET.get('name')

    if name:
        authors = authors.filter(name__icontains=name)

    context = {'authors': authors}

    return render(request, 'author/list_of_authors.html', context=context)


@login_required
@permission_required('is_staff', raise_exception=True)
def create_an_author(request): 
    if request.method == 'POST':
        name = request.POST.get('name','').strip()
        surname = request.POST.get('surname', '').strip()
        patronymic = request.POST.get('patronymic', '').strip()

        if not name:
            messages.error(request, "The name is must be required")
        elif len(name) > 20:
            messages.error(request, "The name of an author must contain fewer than 20 characters.")

        if not surname:
            messages.error(request, "The surname is must be required")
        elif len(surname) > 20:
            messages.error(request, "The surname of an author must contain fewer than 20 characters.")

        if not patronymic:
            messages.error(request, "The patronymic is must be required")
        elif len(patronymic) > 20:
            messages.error(request, "The patronymic of an author must contain fewer than 20 characters.")

        try:
            author = Author.create(name=name, surname=surname, patronymic=patronymic)
        except Exception:
            messages.error(request, "Sorry, something went wrong.")
        else:
            messages.success(request, "The new author successfully created!")
            return redirect('author:author_detail', author_id=author.id)

    return render(request, 'author/create_an_author.html')


@login_required
def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)

    context = {'author': author}

    return render(request,'author/author_detail.html', context=context)


@login_required
@permission_required('is_staff', raise_exception=True)
def delete_an_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)

    if author.books.exists():
        messages.error(request, "Cannot delete an author attached to a book.")
        return redirect('author:author_detail', author_id=author.id)

    if Author.delete_by_id(author_id):
        messages.success(request, "The author successfully deleted!")
    else:
        messages.error(request, "Sorry, something went wrong.")
    return redirect('author:list_of_authors')


@login_required
@permission_required('is_staff', raise_exception=True)
def update_an_author(request, author_id):

    author = get_object_or_404(Author, pk=author_id)

    try:
        if request.method == 'POST':

            author.name = request.POST.get('name', '').strip()
            author.surname = request.POST.get('surname', '').strip()
            author.patronymic = request.POST.get('patronymic', '').strip()

            if not author.name:
                messages.error(request, "The name is must be required")
            elif len(author.name) > 20:
                messages.error(request, "The name of an author must contain fewer than 20 characters.")

            if not author.surname:
                messages.error(request, "The surname is must be required")
            elif len(author.surname) > 20:
                messages.error(request, "The surname of an author must contain fewer than 20 characters.")

            if not author.patronymic:
                messages.error(request, "The patronymic is must be required")
            elif len(author.patronymic) > 20:
                messages.error(request, "The patronymic of an author must contain fewer than 20 characters.")

            author.update(name=author.name, surname=author.surname, patronymic=author.patronymic)
        else:
            context = {'author':author}
            return render(request,'author/update_an_author.html', context=context)

    except Exception:
        messages.error(request, "Sorry, something went wrong.")
    else:
        messages.success(request, "The author successfully updated!")
        return redirect('author:author_detail', author_id=author.id)

    context = {'author':author}

    return render(request,'author/update_an_author.html', context=context)
