import json
import pandas as pd

from django.db.models import Q
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
from main.helper import random_password

def index(request):
    """
    The index view is the view that a user will be redirected to when accessing the website.
    This view is meant to be flexible and currently redirects users to the home view.
    """
    return home(request)

def login_form(request):
    """
    View for users to login.
    When a GET request is send, an empty login form is rendered and returned.
    When a POST request is send, however, the input data is validated and the user will be logged in and redirected to home (which in turn redirects them to their correct home page according to their permissions)
    If the form is not valid, e.g. a wrong password was entered, the form will be populated with the data that was entered up to this point and send back for the user to try again.
    """
    if request.method == 'POST' :
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('main:home'))
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
    """
    Can be called to log a user out.
    Redirects to the login page after logging out.
    """
    logout(request)
    return HttpResponseRedirect(reverse("main:login"))

class OverviewView(PermissionRequiredMixin, generic.ListView):
    """
    An overview only accessible to Therapists that returns a rendered html page with all their clients.
    """
    template_name = 'main/overview.html'
    permission_required = ('auth.is_therapist')
    context_object_name = 'athlete_list'

    def get_queryset(self):
        """
        Return the list of athletes that are registered with the logged-in physiotherapist to populate the context object.
        """
        search_param = self.request.GET.get("q")
        user = self.request.user
        # filtering athletes
        if search_param:
            # the "Q" is just an or
            return Athlete.objects.filter(therapist__auth_user=user).filter(Q(first_name__icontains=search_param) | Q(last_name__icontains=search_param)).order_by('last_name')
        else: # all Athletes
            return Athlete.objects.filter(therapist__auth_user=user).order_by('last_name')
        
        #return Athlete.objects.filter(therapist__auth_user=user).order_by('last_name')

    def get_context_data(self, **kwargs):
        """
        update the context data to include the user object.
        """
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

def athlete(request, pk):
    """
    A view that shows detailed information about an athlete together with a heatmap superimposed on a 3D objects for a user to visualize their training data.
    For security reasons, a logged in Athlete can only access this view with the primary key that corresponds to their user account. A Therapist can only access this view for Athletes that are associated with him.
    """
    athlete = get_object_or_404(Athlete, pk=pk)
    if request.user.has_perm("auth.is_therapist") and not athlete.therapist.auth_user == request.user:
        return HttpResponseRedirect(reverse("main:access-restricted"))
    elif not request.user.has_perm("auth.is_therapist") and athlete.auth_user != request.user:
        return HttpResponseRedirect(reverse("main:access-restricted"))
    context = {
        "athlete": athlete,
    }
    return render(request, 'main/athlete.html', context)

@permission_required("auth.is_therapist")
def add_athlete(request, pk):
    """
    A view that shows a form to create a new athlete. The form is automatically generating a new password and username, stores these values in the session object. Upon valid input the browser will be redirected to main:athlete_added, where they can see the generated password and username so that they can pass these credentials on to their client.
    """
    context = {}
    if request.method == "POST" :
        add_athlete_form = AddAthleteForm(request.POST)   
        if add_athlete_form.is_valid():
            therapist = Therapist.objects.get(auth_user=request.user)
            username = add_athlete_form.cleaned_data['first_name']
            # if there's already a user with that username, add the primary key of the newly created user
            if User.objects.filter(username__startswith=username) is not None:
                username += str(User.objects.all().order_by('-pk')[0].id + 1)
            password = random_password()
            new_auth_user = User.objects.create_user(username=username, password=password)
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
            request.session["recent_password"] = password
            return HttpResponseRedirect(reverse('main:athlete_added'))
        else: 
            messages.error(request, 'error saving athlete')
    
    add_athlete = AddAthleteForm()
    all_athletes = Athlete.objects.all()
    context['add_athlete'] = add_athlete
    context['all_athletes'] = all_athletes
    return render(request, 'main/add_athlete.html', context=context)

def athlete_added(request):
    """
    Display the username and password of a recently added athlete.
    This view is only supposed to be called from add_athlete once a new athlete was added.
    For security reasons, the credentials are taken from the session object.

    """
    context = {
            "username": request.session["recent_username"],
            "password": request.session["recent_password"]
            }
    return render(request, 'main/athlete_added.html', context=context)

def request_workout_details(request, workout_id):
    """
    Returns a JSON object with sensor readings for a workout with id workout_id.
    """
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
    """
    Shows an error message when a user tries to access a page that they don't have access for.
    """
    return HttpResponse("you don't have access to the requested resource")
