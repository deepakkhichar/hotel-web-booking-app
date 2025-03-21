from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from bookings.forms import BookingForm
from bookings.models import Booking
from hotels.models import Room
from notifications.models import Notification


@login_required
def book_room(request: HttpRequest, room_id: int) -> HttpResponse:
    """
    Handle the room booking process.

    This function allows authenticated users to book a room. It validates
    the booking dates, checks room availability, calculates the total price,
    and creates a booking record. It also creates notifications for both
    the customer and hotel owner.

    Args:
        request (HttpRequest): The incoming HTTP request
        room_id (int): The ID of the room to book

    Returns:
        HttpResponse: Redirect to booking list or render booking form
    """
    if not request.user.is_customer:
        messages.error(request, 'Only customers can book rooms.')
        return redirect('home')

    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']

            overlapping_bookings = Booking.objects.filter(
                room=room,
                status__in=['pending', 'confirmed'],
                check_in_date__lt=check_out_date,
                check_out_date__gt=check_in_date,
            )

            if overlapping_bookings.exists():
                messages.error(request, 'Room is not available for the selected dates.')
                return redirect('hotel_detail', hotel_id=room.hotel.id)

            days = (check_out_date - check_in_date).days
            total_price = room.price * days

            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.total_price = total_price
            booking.save()

            Notification.objects.create(
                user=room.hotel.user,
                title='New Booking',
                message=f'You have a new booking from {request.user.username} for {days} ' f'days.',
            )

            messages.success(request, 'Booking successful!')
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'bookings/book_room.html', {'form': form, 'room': room})


@login_required
def confirm_booking(request: HttpRequest, booking_id: int) -> HttpResponse:
    """
    Confirm a pending booking by a hotel owner.

    This function allows hotel owners to confirm bookings made by customers.
    It verifies that the user is authorized to confirm the booking (i.e., they
    own the hotel associated with the booking), updates the booking status to
    'confirmed', and creates a notification for the customer.

    Args:
        request (HttpRequest): The incoming HTTP request
        booking_id (int): The ID of the booking to confirm

    Returns:
        HttpResponse: Redirect to hotel dashboard with success/error message
    """
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user != booking.room.hotel.user:
        messages.error(request, 'You are not authorized to confirm this booking.')
        return redirect('booking_list')

    if booking.status != 'pending':
        messages.error(request, 'This booking cannot be confirmed.')
        return redirect('booking_detail', booking_id=booking.id)

    booking.status = 'confirmed'
    booking.save()

    Notification.objects.create(
        user=booking.user,
        title='Booking Confirmed',
        message=f'Your booking #{booking.id} at {booking.room.hotel.name} has been ' f'confirmed.',
    )

    messages.success(request, 'Booking confirmed successfully.')
    return redirect('hotel_dashboard')


@login_required
def booking_detail(request: HttpRequest, booking_id: int) -> HttpResponse:
    """
    Display detailed information about a specific booking.

    This function retrieves a booking by its ID and displays its details.
    It ensures that only the booking owner or the hotel owner can view
    the booking details.

    Args:
        request (HttpRequest): The incoming HTTP request
        booking_id (int): The ID of the booking to display

    Returns:
        HttpResponse: Rendered booking detail page or redirect to home
    """
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user != booking.user and request.user != booking.room.hotel.user:
        messages.error(request, 'You are not authorized to view this booking.')
        return redirect('home')

    return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required
def booking_list(request: HttpRequest) -> HttpResponse:
    """
    Display a list of bookings for the current user.

    This function retrieves all bookings associated with the current user
    and displays them in a list. For hotel owners, it shows bookings for
    their hotel rooms.

    Args:
        request (HttpRequest): The incoming HTTP request

    Returns:
        HttpResponse: Rendered booking list page
    """
    if request.user.is_customer:
        bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    elif request.user.is_hotel:
        hotel = request.user.hotel_profile
        rooms = Room.objects.filter(hotel=hotel)
        bookings = Booking.objects.filter(room__in=rooms).order_by('-created_at')
    else:
        bookings = []

    return render(request, 'bookings/booking_list.html', {'bookings': bookings})


@login_required
def cancel_booking(request: HttpRequest, booking_id: int) -> HttpResponse:
    """
    Cancel a booking.

    This function allows users to cancel their bookings. It verifies that
    the user is authorized to cancel the booking, updates the booking status
    to 'cancelled', and creates a notification for the hotel owner.

    Args:
        request (HttpRequest): The incoming HTTP request
        booking_id (int): The ID of the booking to cancel

    Returns:
        HttpResponse: Redirect to booking list with success/error message
    """
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user != booking.user and request.user != booking.room.hotel.user:
        messages.error(request, 'You are not authorized to cancel this booking.')
        return redirect('booking_list')

    if booking.status != 'pending' and booking.status != 'confirmed':
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('booking_detail', booking_id=booking.id)

    booking.status = 'cancelled'
    booking.save()

    Notification.objects.create(
        user=booking.room.hotel.user,
        title='Booking Cancelled',
        message=f'Booking #{booking.id} has been cancelled by {request.user.username}.',
    )
    Notification.objects.create(
        user=booking.user,
        title='Booking Cancelled',
        message=f'Booking #{booking.id} has been cancelled by {request.user.username}.',
    )

    messages.success(request, 'Booking cancelled successfully.')
    return redirect('booking_list')
