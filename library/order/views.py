from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from order.models import Order
from book.models import Book
from authentication.models import CustomUser
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.contrib import messages

LOAN_PERIOD = timedelta(weeks=2)

@login_required
def create_an_order(request):
    if request.user.is_staff:
        messages.error(request, "Librarians cannot create orders")
        return render(request, '403.html', status=403)
    
    if request.method == 'POST':
        book_id = request.POST.get('book')
        book = Book.get_by_id(book_id)

        if book is None:
            raise Http404("Book not found")

        plated_end_at = timezone.now() + LOAN_PERIOD
        order = Order.create(user=request.user, book=book, plated_end_at=plated_end_at)

        if order is None:
            books = Book.objects.all()
            return render(request, 'order/create_an_order.html', {'error': 'No copies available.', 'books': books})

        book.count -= 1
        book.save()

        return redirect('user_orders', user_id=request.user.id)

    books = Book.objects.all()
    return render(request, 'order/create_an_order.html', {'books': books})

@login_required
@permission_required('is_staff', raise_exception=True)
def close_an_order(request, order_id):
    order = Order.get_by_id(order_id)
    if order is None:
        raise Http404("Not found")
    if request.method == 'POST':
        order.update(end_at=timezone.now())
        order.book.count += 1
        order.book.save()
        return redirect('list_of_orders')
    return render(request, 'order/close_an_order.html', {'order': order})

@login_required
def user_orders(request, user_id):
    if not request.user.is_staff and request.user.id != user_id:
        messages.error(request, "Not allowed")
        return render(request, '403.html', status=403)

    if request.user.is_staff:
        return redirect(f"/orders/?user={user_id}")

    orders = Order.objects.filter(user_id=user_id)
    return render(request, 'order/user_orders.html', {'orders': orders, 'user_id': user_id})

@login_required
@permission_required('is_staff', raise_exception=True)
def list_of_orders(request):
    orders = Order.objects.all()
    user_id = request.GET.get('user')
    if user_id:
        orders = orders.filter(user_id=user_id)
    return render(request, 'order/list_of_orders.html', {'orders': orders, 'filtered_user_id': user_id})