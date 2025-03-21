# Hotel Management Website

A comprehensive hotel management system that allows hotels to manage their rooms and bookings, and customers to search
for and book hotel rooms.

## Features

- **User Authentication**
    - Customer and Hotel registration and login
    - Profile management

- **Hotel Management**
    - Hotel dashboard for owners
    - Room management (add, edit, delete)
    - Booking management
    - Hotel details editing

- **Customer Features**
    - Search hotels by location, price, and rating
    - View hotel details and rooms
    - Book rooms
    - Manage bookings
    - Receive notifications

- **Maps Integration**
    - View hotel locations on a map
    - Get directions to hotels

## Tech Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite (development), PostgreSQL (production)
- **Maps**: Google Maps API

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hotel-management-website
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a .env file based on .env.example:
   ```bash
   cp .env.example .env
   ```
5. Update the .env file with your configuration:
    - Set `SECRET_KEY` for Django
    - Configure database settings
    - Add your Google Maps API key

6. Run migrations:
   ```bash
   python manage.py migrate
   ```
7. Create a superuser (for admin access):
   ```bash
   python manage.py createsuperuser
   ```
8. Generate sample data (optional):
   ```bash
   python manage.py scrape_hotels
   ```
9. Run the development server:
   ```bash
   python manage.py runserver
   ```
10. Access the website at `http://127.0.0.1:8000/`.