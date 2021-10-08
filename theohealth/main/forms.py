from django.forms import ModelForm
from main.models import Athlete

class AddAthleteForm(ModelForm):
    class Meta:
        model = Athlete
        fields = ['first_name', 'last_name', 'contact_nb', 'email', 'phone_nb', 'injury']