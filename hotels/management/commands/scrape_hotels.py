import random
from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from hotels.models import Hotel

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

        for i in range(20):
            username = f'hotel{i + 1}'
            email = f'hotel{i + 1}@example.com'

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, email=email, password='password123', is_hotel=True)

            hotel_name = f"{random.choice(hotel_prefixes)} {random.choice(hotel_suffixes)}"
            city = random.choice(cities)

            Hotel.objects.get_or_create(
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

        self.stdout.write(self.style.SUCCESS('Successfully created sample hotel data'))
