from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from main.forms import AddAthleteForm, LoginForm
from django.contrib import messages
from main.models import Athlete, Therapist, Workout, SensorReading

# index page
def index(request):
    context = {
            "foo" : "bar",
    }
    return render(request, 'main/index.html', context)

# login page
def login_form(request):
    if request.method == 'POST' :
        login_form = LoginForm(request.POST)
        if login_form.is_valid():

            return HttpResponseRedirect('/overview/')
        else: 
            messages.error(request, 'Error logging in')

    context = {"form":LoginForm()}
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
        add_athlete_form = AddAthleteForm(request.POST)   
        if add_athlete_form.is_valid():
            default_therapist = Therapist.objects.get(pk=1)
            new_athlete = Athlete.objects.create(
                therapist = default_therapist,
                first_name = add_athlete_form.cleaned_data['first_name'],
                last_name = add_athlete_form.cleaned_data['last_name'],
                contact_nb = add_athlete_form.cleaned_data['contact_nb'],
                email = add_athlete_form.cleaned_data['email'],
                phone_nb = add_athlete_form.cleaned_data['phone_nb'],
                injury = add_athlete_form.cleaned_data['injury'],
            )
            messages.success(request, 'Athlete added successfully')
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


def request_workout_details(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id)
    all_readings = workout.readings_from_file()
    #context = {'plotted_graph': plotted_graph}
    return HttpResponse(all_readings)
    #return render(request, 'main/view_graph.html', context)