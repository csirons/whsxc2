from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from blog.models import Entry


def index(request):
    return render(request, "blog/entry_archive.html",  {
            "latest": Entry.objects.all().order_by("-created_at")[:5],
            #datelist:
        },)


