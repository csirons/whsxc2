from django.http import HttpResponsePermanentRedirect
from django.views.generic import TemplateView # direct_to_template is deprecated, use TemplateView instead
from django.shortcuts import render
from blog.models import Entry
from runners.models import *

def homepage(request):
    # return HttpResponse("Hello, world. You're at homepage.")
    return render(request, 'home.html', {
            "latest": Entry.objects.all().order_by("-created_at")[:5],
            #datelist:
        },)

def archive(request):
    return render(request, "blog/entry_archive.html",  {
            "latest": Entry.objects.all().order_by("-created_at")[:5],
            #datelist:
        },)

def runners(request):
    #def runners_list(request):
    # calculate which years have runners
    years = Meet.objects.years()
    actual_years = []
    runners_by_year = {}
    for year in years:
        runners = Runner.people.by_year(year)
        if len(runners) > 0:
            runners_by_year[year] = runners
            actual_years.append(year)
    #actual_years =['2002', '2001', '2000']  # Example data for testing, replace with actual years from the database
    #runners_by_year={'2000': ['Bob', 'Alice'], '2001': ['Charlie'], '2002': ['David']}  # Example data for testing
    return render(request,'runners/runners.html', {
        "runners_by_year": runners_by_year,  # Sort years in descending order
        "years": actual_years,
         },)
    #return render(request, 'runners/runners.html', {
    #        "years_list": MeetManager.years('self'),  # Assuming MeetManager has a method to get years
    #        #datelist:
    #    },)

def meets(request):
    return render(request, 'meets/meets.html', {
            "latest": Entry.objects.all().order_by("-created_at")[:5],
            #datelist:
        },)

def history(request):
    return render(request, 'history/history.html', {
            "latest": Entry.objects.all().order_by("-created_at")[:5],
            #datelist:
        },)

def schedule(request):
    return render(request, 'schedule/schedule.html', {
            "latest": Entry.objects.all().order_by("-created_at")[:5],
            #datelist:
        },)

def homemeet(request):
    return render(request, 'homemeet/homemeet.html', {
            "latest": Entry.objects.all().order_by("-created_at")[:5],
            #datelist:
        },)

def runninglinks(request):
    return render(request, 'runninglinks/runninglinks.html', {
            "latest": Entry.objects.all().order_by("-created_at")[:5],
            #datelist:
        },)

def summerrunning(request):
    return render(request, 'summerrunning/summerrunning.html', {
            "latest": Entry.objects.all().order_by("-created_at")[:5],
            #datelist:
        },)