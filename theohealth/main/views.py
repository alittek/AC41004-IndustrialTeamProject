from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

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
def overview(request, pk):
    context = {
        "foo" : "bar",
    }
    return render(request, 'main/overview.html', context)

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
