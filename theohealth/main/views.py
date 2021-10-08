from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import generic

from main.models import Athlete, Therapist
from main.forms import AddAthleteForm
from django.contrib import messages

# index page
def index(request):
    context = {
            "foo" : "bar",
    }
    return render(request, 'main/index.html', context)

# login page
def login(request):
    context = {
        "foo" : "bar",
    }
    return render(request, 'main/login.html', context)

# overview all athletes page
class OverviewView(generic.ListView):
    template_name = 'main/overview.html'
    context_object_name = 'athlete_list'

    def get_queryset(self):
        """
        Return the list of athletes that are registered with the logged-in physiotherapist
        """
        return Athlete.objects.all()

# heatmap & info for one athlete
def athlete(request, pk):
    context = {
        "foo" : "bar",
    }
    return render(request, 'main/athlete.html', context)

# page to add a new athlete
def add_athlete(request, pk):
    if request.method == "POST" :
        add_athlete = AddAthleteForm(request.POST)   
        if add_athlete.is_valid():
            default_therapist = Therapist.objects.get(pk=1)
            new_athlete = Athlete.objects.create(
                therapist = default_therapist,
                first_name = add_athlete.cleaned_data['first_name'],
                last_name = add_athlete.cleaned_data['last_name'],
                contact_nb = add_athlete.cleaned_data['contact_nb'],
                email = add_athlete.cleaned_data['email'],
                phone_nb = add_athlete.cleaned_data['phone_nb'],
                injury = add_athlete.cleaned_data['injury'],
            )
            messages.success(request, ('Athlete added successfully'))
        else: 
            messages.error(request, 'Error saving athlete')
    
    add_athlete = AddAthleteForm()
    all_athletes = Athlete.objects.all()
    return render(request, 'main/add_athlete.html', context={'add_athlete':add_athlete, 'all_athletes':all_athletes})

# instruct server to add new athlete
def post_athlete(request):
    context = {
        "foo" : "bar",
    }
    return render(request, 'main/add_athlete.html', context)
