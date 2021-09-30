from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {
            "joke_of_the_day": "What happens when a computer engineer fails flirting with a waitress? Error in connecting to the server",
            "cities" : ["Dundee", "Aberdeen", "Glasgow", "Edinburgh", "Inverness"],
            "foo" : "bar",
            }
    return render(request, 'playground/index.html', context)

def test(request):
    context = {
            "foo" : "bar",
            }
    return render(request, 'playground/test.html', context)

def test1(request):
    context = {
            "foo" : "bar",
            }
    return render(request, 'playground/test1.html', context)
