from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from accounts.forms import CustomerRegistrationForm, HotelRegistrationForm
from hotels.models import Hotel


def customer_register(request: HttpRequest) -> HttpResponse:
    """
    Handle customer registration process.

    This function processes the customer registration form, creates a new user
    account with customer privileges, and logs the user in upon successful
    registration. It handles both GET requests (displaying the form) and POST
    requests (processing form submission).

    Args:
        request (HttpRequest): The incoming HTTP request

    Returns:
        HttpResponse: Rendered registration page or redirect to home
    """
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'user_type': 'customer'})


def hotel_register(request: HttpRequest) -> HttpResponse:
    """
    Handle hotel registration process.

    This function processes the hotel registration form, creates a new user
    account with hotel privileges, and creates a corresponding hotel profile.
    It handles both GET requests (displaying the form) and POST requests
    (processing form submission). Upon successful registration, it logs the
    user in and redirects to the home page.

    Args:
        request (HttpRequest): The incoming HTTP request

    Returns:
        HttpResponse: Rendered registration page or redirect to home
    """
    if request.method == 'POST':
        form = HotelRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            hotel = Hotel.objects.create(
                user=user,
                name=form.cleaned_data['hotel_name'],
                description=form.cleaned_data['hotel_description'],
                address=form.cleaned_data['hotel_address'],
                city=form.cleaned_data['hotel_city'],
                state=form.cleaned_data['hotel_state'],
                country=form.cleaned_data['hotel_country'],
                zip_code=form.cleaned_data['hotel_zip_code'],
                price_per_night=form.cleaned_data['hotel_price_per_night'],
                latitude=form.cleaned_data['hotel_latitude'],
                longitude=form.cleaned_data['hotel_longitude'],
            )
            if 'hotel_image' in request.FILES:
                hotel.image = request.FILES['hotel_image']
                hotel.save()

            login(request, user)
            messages.success(request, 'Hotel registration successful!')
            return redirect('home')
    else:
        form = HotelRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'user_type': 'hotel'})


def custom_logout(request: HttpRequest) -> HttpResponse:
    """
    Handle user logout process.

    This function logs out the current user and redirects them to the home page
    with a success message.

    Args:
        request (HttpRequest): The incoming HTTP request

    Returns:
        HttpResponse: Redirect to home page
    """
    logout(request)
    return redirect('home')


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    """
    Display and update user profile information.

    This function handles both displaying the user's profile information and
    processing form submissions to update that information. It differentiates
    between hotel users and regular users to display appropriate profile fields.

    Args:
        request (HttpRequest): The incoming HTTP request

    Returns:
        HttpResponse: Rendered profile page or redirect after update
    """

    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.phone = request.POST.get('phone', '')
        user.address = request.POST.get('address', '')

        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if password and confirm_password:
            if password == confirm_password:
                user.set_password(password)
                messages.success(request, 'Password updated successfully.')
            else:
                messages.error(request, 'Passwords do not match.')
                return redirect('profile')

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'accounts/profile.html')
