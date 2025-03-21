from django.contrib import admin

from hotels.models import Hotel, Room


class RoomInline(admin.TabularInline):
    model = Room
    extra = 1


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'rating', 'price_per_night')
    list_filter = ('city', 'country', 'rating')
    search_fields = ('name', 'city', 'country')
    inlines = [RoomInline]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_type', 'price', 'capacity', 'available')
    list_filter = ('room_type', 'available', 'hotel')
    search_fields = ('hotel__name',)
