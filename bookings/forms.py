from datetime import date

from django import forms

from bookings.models import Booking


class BookingForm(forms.ModelForm):
    check_in_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': date.today().isoformat()}))
    check_out_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': date.today().isoformat()}))

    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date']

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        if check_in_date and check_out_date:
            if check_in_date >= check_out_date:
                raise forms.ValidationError("Check-out date must be after check-in date.")

            if check_in_date < date.today():
                raise forms.ValidationError("Check-in date cannot be in the past.")

        return cleaned_data
