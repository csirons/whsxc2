"""
URL configuration for whsxc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.base import TemplateView

from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

from blog.models import Entry
from blog import views 
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),  
    path('',views.homepage),
    path('runners/',views.runners),
    path('meets/',views.meets),
    path('history/', views.history),
    path('archive/', views.archive),
    path('schedule/', views.schedule),
    path('homemeet/', views.homemeet),
    path('runninglinks/', views.runninglinks),
    path('summerrunning/info/', views.summerrunning),
    path('meets/<int:object_id>/', views.meet_detail),
    path('meets/<int:object_id>/sort-<str:sort>/', views.meet_detail),
    path('meets/<int:object_id>/', views.meet_detail ),
    path('courses/', views.courses_list),
    path('courses/<int:object_id>/', views.course_detail),
    path('top10/', views.top10_list),
    path('runners/<int:object_id>/', views.runner_detail), # tiis is new, was not on the original
    path('runners/<int:object_id>/(organize-<str:organize>/)?', views.runner_detail),
    path('runners/<int:object_id>/(organize-<str:organize>/)?sort-<str:sort>/', views.runner_detail),
]
 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

