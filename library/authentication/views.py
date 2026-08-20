from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required

from authentication.models import CustomUser

def index_view(request):
    return render(request, 'authentication/index.html')


def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('authentication:profile')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = CustomUser.objects.create_user(
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                middle_name=data.get('middle_name', ''),
                role=data['role'],
                is_active=True
            )

            login(request, new_user)
            messages.success(request, 'Registration has been successful!')
            return redirect('authentication:index_auth')
    else:
        form = RegisterForm()

    return render(request, 'authentication/register.html', {'form': form})


def login_view(request):

    if request.user.is_authenticated:
        messages.info(request, "You are already logged")
        return redirect('authentication:profile')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, email=email, password=password)

        if user is not None:

            login(request, user)

            messages.success(request, f'Congratulation, {user.email}!')
            return redirect('authentication:index_auth')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'authentication/login.html')


@login_required
def logout_view(request):

    logout(request)

    messages.success(request, "Logged out")
    return redirect('authentication:index_auth')


@login_required
def profile_view(request):
    context = {'user_obj': request.user}
    return render(request, 'authentication/profile.html', context=context)


@login_required
def update_profile(request, user_id):

    user = get_object_or_404(CustomUser, pk=user_id)

    try:
        if user != request.user:
            raise Exception

        if request.method == 'POST':

            user.first_name = request.POST.get('first_name', '').strip()
            user.middle_name = request.POST.get('middle_name', '').strip()
            user.last_name = request.POST.get('last_name', '').strip()
            password = request.POST.get('password', '').strip()

            if not user.first_name:
                messages.error(request, "The first_name is must be required")
            elif len(user.first_name) > 20:
                messages.error(request, "The first_name of a user must contain fewer than 20 characters.")

            if not user.middle_name:
                messages.error(request, "The middle_name is must be required")
            elif len(user.middle_name) > 20:
                messages.error(request, "The middle_name of a user must contain fewer than 20 characters.")

            if not user.last_name:
                messages.error(request, "The last_name is must be required")
            elif len(user.last_name) > 20:
                messages.error(request, "The last_name of a user must contain fewer than 20 characters.")

            if not password or not password.strip():
                password = None

            updated_user = user.update(first_name=user.first_name, middle_name=user.middle_name, last_name=user.last_name, password=password)

            if password and updated_user:
                user.refresh_from_db()
                update_session_auth_hash(request, updated_user)
        else:
            context = {'user':user}
            return render(request,'authentication/update_profile.html', context=context)

    except Exception:
        messages.error(request, "Sorry, something went wrong.")
    else:
        messages.success(request, "The user successfully updated!")
        return redirect('authentication:profile')

    context = {'user':user}

    return render(request,'authentication/update_profile.html', context=context)


@login_required
@permission_required('is_staff', raise_exception=True)
def list_of_users_view(request):
    
    users = CustomUser.objects.all()

    context = {'users': users}

    return render(request, 'authentication/list_of_users.html', context=context)


@login_required
@permission_required('is_staff', raise_exception=True)
def user_details_view(request, user_id):

    user = get_object_or_404(CustomUser, pk=user_id)

    context = {'user_obj': user}

    return render(request, 'authentication/user_details.html', context=context)

def bad_request(request, exception=None):
    return render(request, '400.html', status=400)

def permission_denied(request, exception=None):
    return render(request, '403.html', status=403)

def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)

def server_error(request):
    return render(request, '500.html', status=500)