import os
import random
from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand

from hotels.models import Hotel, Room

User = get_user_model()


class Command(BaseCommand):
    """
    Django management command to generate sample hotel data.

    This command creates sample hotel data with random attributes such as names,
    locations, and prices. It's useful for populating the database with test data
    during development and testing phases.
    """

    help = 'Scrape hotel data from websites'

    def handle(self, *args: Any, **kwargs: Any) -> None:
        """
        Execute the command to generate sample hotel data.

        This method creates multiple hotel users and their corresponding hotel
        profiles with randomized data including names, locations, and prices.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """

        self.stdout.write('Creating sample hotel data...')

        cities = ['New York', 'Los Angeles', 'Chicago', 'San Francisco', 'Miami', 'Boston', 'Seattle']

        hotel_prefixes = ['Grand', 'Royal', 'Luxury', 'Elite', 'Premium', 'Comfort', 'Sunset']
        hotel_suffixes = ['Hotel', 'Resort', 'Suites', 'Inn', 'Lodge', 'Plaza', 'Palace']

        room_types = {'single': (80, 150), 'double': (120, 250), 'suite': (200, 400), 'deluxe': (300, 600)}
        sample_images_dir = os.path.join(settings.BASE_DIR, 'media', 'sample_hotel_images')
        hotel_images = []
        if os.path.exists(sample_images_dir):
            hotel_images = [f for f in os.listdir(sample_images_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        if not hotel_images:
            self.stdout.write(self.style.WARNING('No hotel sample images found in media/sample_hotel_images/'))

        for i in range(20):
            username = f'hotel{i + 1}'
            email = f'hotel{i + 1}@example.com'

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, email=email, password='password123', is_hotel=True)

            hotel_name = f"{random.choice(hotel_prefixes)} {random.choice(hotel_suffixes)}"
            city = random.choice(cities)

            hotel, created = Hotel.objects.get_or_create(
                user=user,
                defaults={
                    'name': hotel_name,
                    'description': f"A beautiful hotel located in {city}.",
                    'address': f"{random.randint(100, 999)} Main Street",
                    'city': city,
                    'state': 'State',
                    'country': 'USA',
                    'zip_code': f"{random.randint(10000, 99999)}",
                    'latitude': random.uniform(25.0, 48.0),
                    'longitude': random.uniform(-125.0, -70.0),
                    'price_per_night': random.randint(80, 500),
                    'rating': round(random.uniform(3.0, 5.0), 1),
                },
            )

            if hotel_images and not hotel.image:
                image_path = os.path.join(sample_images_dir, random.choice(hotel_images))
                with open(image_path, 'rb') as img_file:
                    hotel.image.save(os.path.basename(image_path), File(img_file), save=True)
                self.stdout.write(f'Added image to hotel {hotel.name}')

            if created or Room.objects.filter(hotel=hotel).count() == 0:
                for room_type, price_range in room_types.items():
                    for _ in range(random.randint(1, 3)):
                        price = random.randint(price_range[0], price_range[1])
                        capacity = 1 if room_type == 'single' else 2 if room_type == 'double' else random.randint(2, 4)

                        Room.objects.create(
                            hotel=hotel,
                            room_type=room_type,
                            price=price,
                            capacity=capacity,
                            available=random.choice([True, True, True, False]),  # 75% chance of being available
                        )

                self.stdout.write(f'Created rooms for hotel {hotel.name}')

        self.stdout.write(self.style.SUCCESS('Successfully created sample hotel data'))
