# from django.http import HttpResponse
from django.shortcuts import render
from blog.models import Entry
from runners.models import RunnerManager, Runner, MeetManager, Meet

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
    return render(request, 'runners/runners.html', {
            "latest": Entry.objects.all().order_by("-created_at")[:5],
            #datelist:
        },)

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