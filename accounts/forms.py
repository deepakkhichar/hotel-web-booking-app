from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class CustomerRegistrationForm(UserCreationForm):
    """
    Form for customer registration.

    Extends Django's UserCreationForm to include additional fields
    and set the is_customer flag to True.
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        if commit:
            user.save()
        return user


class HotelRegistrationForm(UserCreationForm):
    """
    Form for hotel registration.

    Extends Django's UserCreationForm to include hotel-specific fields
    and set the is_hotel flag to True.
    """

    email = forms.EmailField(required=True)

    hotel_name = forms.CharField(max_length=100, required=True)
    hotel_description = forms.CharField(widget=forms.Textarea, required=True)
    hotel_address = forms.CharField(max_length=255, required=True)
    hotel_city = forms.CharField(max_length=100, required=True)
    hotel_state = forms.CharField(max_length=100, required=True)
    hotel_country = forms.CharField(max_length=100, required=True)
    hotel_zip_code = forms.CharField(max_length=20, required=True)
    hotel_price_per_night = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    hotel_latitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False)
    hotel_longitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False)
    hotel_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_hotel = True
        if commit:
            user.save()
        return user
