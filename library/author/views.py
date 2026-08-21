from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from author.models import Author
from .forms import AuthorForm, AuthorFilterForm

app_name = 'author'

@login_required
@permission_required('is_staff', raise_exception=True)
def list_of_authors(request):
    authors = Author.objects.all()
    form = AuthorFilterForm(request.GET)

    if form.is_valid():
        name = form.cleaned_data.get('name')
        if name:
            authors = authors.filter(name__icontains=name)

    context = {
        'authors': authors,
        'form': form,
    }

    return render(request, 'author/list_of_authors.html', context=context)


@login_required
@permission_required('is_staff', raise_exception=True)
def create_an_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            messages.success(request, "The new author successfully created!")
            return redirect('author:author_detail', author_id=author.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AuthorForm()

    return render(request, 'author/create_an_author.html', {'form': form})

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

    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            messages.success(request, "The author was successfully updated!")
            return redirect('author:author_detail', author_id=author.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AuthorForm(instance=author)

    return render(request, 'author/update_an_author.html', {'form': form, 'author': author})