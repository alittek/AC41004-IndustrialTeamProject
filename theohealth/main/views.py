import json
import pandas as pd

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.template import RequestContext
from django.urls import reverse

from main.forms import AddAthleteForm, LoginForm
from main.models import Athlete, Therapist, Workout, SensorReading

# index page
def index(request):
    context = {
            "foo" : "bar",
            "session": request.session,
            "user": request.user,
    }
    return render(request, 'main/index.html', context)

# login page
def login_form(request):
    if request.method == 'POST' :
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('main:home'))
                """
                if user.has_perm('auth.is_therapist'):
                    return HttpResponseRedirect(reverse('main:overview', kwargs={'pk': 1}))
                else:
                    return HttpResponseRedirect(reverse('main:athlete', kwargs={'pk': 1}))
                    """
            else:
                error = "invalid username or password"
                return render(request, 'main/login.html', {'form': form, 'error': error})
            return HttpResponseRedirect('/overview/')
        else: 
            error = "error loggin in"

    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form':form})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("main:login"))

# overview all athletes page
class OverviewView(PermissionRequiredMixin, generic.ListView):
    template_name = 'main/overview.html'
    permission_required = ('auth.is_therapist')
    context_object_name = 'athlete_list'

    def get_queryset(self):
        """
        Return the list of athletes that are registered with the logged-in physiotherapist
        """
        user = self.request.user
        return Athlete.objects.filter(therapist__auth_user=user).order_by('last_name')

    def get_context_data(self, **kwargs):
        """
        update the context data to include the user object
        """
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

# heatmap & info for one athlete
def athlete(request, pk):
    athlete = get_object_or_404(Athlete, pk=pk)
    if request.user.has_perm("auth.is_therapist") and not athlete.therapist.auth_user == request.user:
        return HttpResponseRedirect(reverse("main:access-restricted"))
    elif not request.user.has_perm("auth.is_therapist") and athlete.auth_user != request.user:
        return HttpResponseRedirect(reverse("main:access-restricted"))
    context = {
        "foo" : "bar",
        "athlete": athlete,
    }
    return render(request, 'main/athlete.html', context)

# page to add a new athlete
@permission_required("auth.is_therapist")
def add_athlete(request, pk):
    context = {}
    if request.method == "POST" :
        add_athlete_form = AddAthleteForm(request.POST)   
        if add_athlete_form.is_valid():
            therapist = Therapist.objects.get(auth_user=request.user)
            username = add_athlete_form.cleaned_data['first_name']
            # if there's already a user with that username, add the primary key of the newly created user)
            if User.objects.filter(username__startswith=username) is not None:
                username += str(User.objects.all().order_by('-pk')[0].id + 1)
            new_auth_user = User.objects.create_user(username=username, password="password")
            new_auth_user.user_permissions.add(Permission.objects.get(codename='is_athlete', content_type=ContentType.objects.get_for_model(User)))
            new_athlete = Athlete.objects.create(
                therapist = therapist,
                auth_user=new_auth_user,
                first_name = add_athlete_form.cleaned_data['first_name'],
                last_name = add_athlete_form.cleaned_data['last_name'],
                contact_nb = add_athlete_form.cleaned_data['contact_nb'],
                email = add_athlete_form.cleaned_data['email'],
                phone_nb = add_athlete_form.cleaned_data['phone_nb'],
                injury = add_athlete_form.cleaned_data['injury'],
            )
            messages.success(request, 'athlete added successfully')
            request.session["recent_username"] = username
            request.session["recent_password"] = "password"
            return HttpResponseRedirect(reverse('main:athlete_added'))
        else: 
            messages.error(request, 'error saving athlete')
    
    add_athlete = AddAthleteForm()
    all_athletes = Athlete.objects.all()
    context['add_athlete'] = add_athlete
    context['all_athletes'] = all_athletes
    return render(request, 'main/add_athlete.html', context=context)

def athlete_added(request):
    context = {
            "username": request.session["recent_username"],
            "password": request.session["recent_password"]
            }
    return render(request, 'main/athlete_added.html', context=context)

# instruct server to add new athlete
def post_athlete(request):
    context = {
        "foo" : "bar",
    }
    return render(request, 'main/add_athlete.html', context)

# Workout details for the purpose of updating the heatmap
def request_workout_details(request, workout_id):
    if Workout.objects.filter(pk=workout_id):
        workout = Workout.objects.get(pk=workout_id)
        all_readings = workout.readings_from_file()
        context = {'all_readings': all_readings}
        return HttpResponse(all_readings)
    else:
        return HttpResponse(":(")

def workout(request):
    readings = []
    for i in range(1, 5):
        # Must use path from the Python shell (manage.py), not from /main!
        df = pd.read_csv('main/SensorTest-set2/SensorTest-sensor' + str(i) + '.csv')
        values = []
        # Zips the columns together so the time and value can be accessed together
        [values.append(record) for record in zip(df.time, df.value)]
        # Appends as sensor(num)
        readings.append(values)

    return HttpResponse(json.dumps(readings))

def home(request):
    """
    Redirects a user to the correct homepage depending on their permissions.
    For instance, a Physiotherapist would be redirected to the athletes' overview page located at main:overview, whereas an athlete would be redirected to their profie/heatmap view.
    This function is also meant to be called after logging in to redirect the user to their correct homepage.
    """
    if request.user.has_perm('auth.is_therapist'):
        return HttpResponseRedirect(reverse('main:overview', kwargs={'pk': 1}))
    elif request.user.has_perm('auth.is_athlete'):
        pk = Athlete.objects.get(auth_user=request.user).id
        return HttpResponseRedirect(reverse('main:athlete', kwargs={'pk': pk}))
    else:
        return HttpResponseRedirect(reverse('main:login'))

def access_restricted(request):
    return HttpResponse("you don't have access to the requested resource")
