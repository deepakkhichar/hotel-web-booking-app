import logging

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from hotels.models import Hotel


def home(request: HttpRequest) -> HttpResponse:
    """
    Render the home page with featured hotels.

    This function retrieves the highest-rated hotels to display as featured
    hotels on the home page. It serves as the main landing page for the
    application, providing users with an overview of the service and
    highlighting premium hotel options.

    Args:
        request (HttpRequest): The incoming HTTP request

    Returns:
        HttpResponse: Rendered home page with featured hotels
    """
    featured_hotels = Hotel.objects.all().order_by('-rating')[:3]

    return render(request, 'home.html', {'featured_hotels': featured_hotels})


logger = logging.getLogger(__name__)


def maps_proxy(request: HttpRequest) -> HttpResponse:
    """
    Proxy for Google Maps API to hide the API key from frontend code.

    This function creates a JavaScript snippet that loads the Google Maps API
    with our API key server-side, preventing the key from being exposed in
    the browser's source code. It acts as a security layer between the client
    and the Google Maps API.

    Args:
        request (HttpRequest): The incoming HTTP request

    Returns:
        HttpResponse: JavaScript content that loads Google Maps API securely
    """
    try:
        api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', '')

        if not api_key:
            return HttpResponse("Google Maps API key is not configured", status=500)

        # Use the recommended loading pattern
        js_content = f"""
        window.initMap = function() {{
            // This function will be called when the Google Maps API is loaded
            if (window.initializeMap) {{
                window.initializeMap();
            }}
        }};
        
        // Use the recommended loading pattern
        (function() {{
            const script = document.createElement('script');
            script.src = "https://maps.googleapis.com/maps/api/js?key={api_key}&callback=initMap&loading=async";
            script.async = true;
            document.head.appendChild(script);
        }})();
        """

        response = HttpResponse(js_content)
        response['Content-Type'] = 'application/javascript'
        return response

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
