from django.shortcuts import render
import pandas as pd
import os
from django.http import HttpResponse
from django.views import generic

from main.models import Athlete, Therapist


# def index(request):
#     THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#     my_file = os.path.join(THIS_FOLDER, 'SensorTest-sensor1.csv')
#     test = pd.read_csv (my_file)
#     return HttpResponse("<h1>Hello Alina!</h1>. This is the <b>polls</b> index")


# index page
def index(request):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'SensorTest-sensor1.csv')
    output = pd.read_csv (my_file)

    context = {
            "foo" : "bar",
    }
    return render(request, 'main/index.html', context, {'output': output})

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
    context = {
        "foo" : "bar",
    }
    return render(request, 'main/add_athlete.html', context)

# instruct server to add new athlete
def post_athlete(request):
    context = {
        "foo" : "bar",
    }
    return render(request, 'main/add_athlete.html', context)
