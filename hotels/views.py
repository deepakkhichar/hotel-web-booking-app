from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from hotels.models import Hotel, Room


def hotel_list(request: HttpRequest) -> HttpResponse:
    """
    Display a list of hotels with search and filtering capabilities.

    This function retrieves hotels from the database and applies filters based
    on user input. It supports searching by hotel name and filtering by city,
    country, rating, and maximum price. The function also provides unique city
    and country options for the filter dropdowns.

    Args:
        request (HttpRequest): The incoming HTTP request containing filter parameters

    Returns:
        HttpResponse: Rendered page with filtered hotel list and filter options
    """
    hotels = Hotel.objects.all()

    search_query = request.GET.get('search', '')
    if search_query:
        hotels = hotels.filter(name__icontains=search_query)

    city = request.GET.get('city', '')
    if city:
        hotels = hotels.filter(city=city)

    country = request.GET.get('country', '')
    if country:
        hotels = hotels.filter(country=country)

    rating = request.GET.get('rating', '')
    if rating:
        hotels = hotels.filter(rating__gte=rating)

    max_price = request.GET.get('max_price', '')
    if max_price:
        hotels = hotels.filter(price_per_night__lte=max_price)

    cities = Hotel.objects.values_list('city', flat=True).distinct()
    countries = Hotel.objects.values_list('country', flat=True).distinct()

    context = {
        'hotels': hotels,
        'cities': cities,
        'countries': countries,
    }

    return render(request, 'hotels/hotel_list.html', context)


def hotel_detail(request: HttpRequest, hotel_id: int) -> HttpResponse:
    """
    Display detailed information about a specific hotel.

    This function retrieves a hotel by its ID and displays its details along
    with the available rooms. It provides comprehensive information about the
    hotel and its accommodation options to help users make booking decisions.

    Args:
        request (HttpRequest): The incoming HTTP request
        hotel_id (int): The ID of the hotel to display

    Returns:
        HttpResponse: Rendered hotel detail page with hotel and room information
    """
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel)
    return render(request, 'hotels/hotel_detail.html', {'hotel': hotel, 'rooms': rooms})


@login_required
def hotel_dashboard(request: HttpRequest) -> HttpResponse:
    """
    Display the hotel owner's dashboard.

    This function provides hotel owners with a dashboard to manage their hotel,
    including viewing and managing rooms and bookings. It verifies that the user
    is a hotel owner, retrieves the hotel profile and associated rooms and bookings,
    and displays them in the dashboard.

    Args:
        request (HttpRequest): The incoming HTTP request

    Returns:
        HttpResponse: Rendered dashboard page or redirect to home for non-hotel users
    """
    if not request.user.is_hotel:
        return redirect('home')

    hotel = get_object_or_404(Hotel, user=request.user)
    rooms = Room.objects.filter(hotel=hotel)
    bookings = []

    for room in rooms:
        bookings.extend(room.bookings.all())

    return render(request, 'hotels/hotel_dashboard.html', {'hotel': hotel, 'rooms': rooms, 'bookings': bookings})


@login_required
def edit_hotel(request: HttpRequest) -> HttpResponse:
    """
    Allow hotel owners to edit their hotel details.

    This function handles the editing of hotel information by hotel owners.
    It verifies that the user is a hotel owner, retrieves the hotel profile,
    and processes form submissions to update hotel details including name,
    description, address, coordinates, and image.

    Args:
        request (HttpRequest): The incoming HTTP request

    Returns:
        HttpResponse: Rendered edit form or redirect to dashboard
    """
    if not request.user.is_hotel:
        messages.error(request, 'Only hotels can edit their details.')
        return redirect('home')

    hotel = get_object_or_404(Hotel, user=request.user)

    if request.method == 'POST':
        hotel.name = request.POST.get('name')
        hotel.description = request.POST.get('description')
        hotel.address = request.POST.get('address')
        hotel.city = request.POST.get('city')
        hotel.state = request.POST.get('state')
        hotel.country = request.POST.get('country')
        hotel.zip_code = request.POST.get('zip_code')
        hotel.price_per_night = request.POST.get('price_per_night')
        hotel.latitude = request.POST.get('latitude') or None
        hotel.longitude = request.POST.get('longitude') or None

        # Handle image upload
        if 'image' in request.FILES:
            hotel.image = request.FILES['image']

        hotel.save()
        messages.success(request, 'Hotel details updated successfully.')
        return redirect('hotel_dashboard')

    return render(request, 'hotels/edit_hotel.html', {'hotel': hotel})


@login_required
def add_room(request: HttpRequest) -> HttpResponse:
    """
    Allow hotel owners to add new rooms to their hotel.

    This function handles the creation of new rooms by hotel owners. It verifies
    that the user is a hotel owner, processes the form data, and creates a new
    room associated with the hotel.

    Args:
        request (HttpRequest): The incoming HTTP request

    Returns:
        HttpResponse: Redirect to hotel dashboard
    """
    if not request.user.is_hotel:
        messages.error(request, 'Only hotels can add rooms.')
        return redirect('home')

    if request.method == 'POST':
        hotel = get_object_or_404(Hotel, user=request.user)
        room_type = request.POST.get('room_type')
        price = request.POST.get('price')
        capacity = request.POST.get('capacity')
        available = request.POST.get('available') == 'on'

        Room.objects.create(hotel=hotel, room_type=room_type, price=price, capacity=capacity, available=available)

        messages.success(request, 'Room added successfully.')
        return redirect('hotel_dashboard')

    return redirect('hotel_dashboard')


@login_required
def edit_room(request: HttpRequest, room_id: int) -> HttpResponse:
    """
    Allow hotel owners to edit room details.

    This function handles the editing of room information by hotel owners.
    It verifies that the user is a hotel owner and that they own the room
    being edited, then processes form submissions to update room details.

    Args:
        request (HttpRequest): The incoming HTTP request
        room_id (int): The ID of the room to edit

    Returns:
        HttpResponse: Rendered edit form or redirect to dashboard
    """
    if not request.user.is_hotel:
        messages.error(request, 'Only hotels can edit rooms.')
        return redirect('home')

    room = get_object_or_404(Room, id=room_id)

    if room.hotel.user != request.user:
        messages.error(request, 'You do not have permission to edit this room.')
        return redirect('hotel_dashboard')

    if request.method == 'POST':
        room.room_type = request.POST.get('room_type')
        room.price = request.POST.get('price')
        room.capacity = request.POST.get('capacity')
        room.available = request.POST.get('available') == 'on'
        room.save()

        messages.success(request, 'Room updated successfully.')
        return redirect('hotel_dashboard')

    return render(request, 'hotels/edit_room.html', {'room': room})


@login_required
def delete_room(request: HttpRequest, room_id: int) -> HttpResponse:
    """
    Allow hotel owners to delete rooms.

    This function handles the deletion of rooms by hotel owners. It verifies
    that the user is a hotel owner and that they own the room being deleted,
    then deletes the room from the database.

    Args:
        request (HttpRequest): The incoming HTTP request
        room_id (int): The ID of the room to delete

    Returns:
        HttpResponse: Redirect to hotel dashboard
    """
    if not request.user.is_hotel:
        messages.error(request, 'Only hotels can delete rooms.')
        return redirect('home')

    room = get_object_or_404(Room, id=room_id)

    if room.hotel.user != request.user:
        messages.error(request, 'You do not have permission to delete this room.')
        return redirect('hotel_dashboard')

    room.delete()
    messages.success(request, 'Room deleted successfully.')
    return redirect('hotel_dashboard')


@login_required
def room_data(request: HttpRequest, room_id: int) -> JsonResponse:
    """
    Return room data as JSON for AJAX requests.

    This function retrieves room data and returns it as JSON for use in
    the edit room modal on the hotel dashboard.

    Args:
        request (HttpRequest): The incoming HTTP request
        room_id (int): The ID of the room to retrieve data for

    Returns:
        JsonResponse: Room data in JSON format
    """
    room = get_object_or_404(Room, id=room_id)

    if room.hotel.user != request.user:
        return JsonResponse({'error': 'Not authorized'}, status=403)

    data = {'room_type': room.room_type, 'price': room.price, 'capacity': room.capacity, 'available': room.available}

    return JsonResponse(data)
