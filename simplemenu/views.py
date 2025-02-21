from whsxc.crosscountry.models import Runner, Meet
from django.contrib.admin.views.main import change_stage, add_stage, delete_stage
from generator import quick_publish

import threading

class QuickPublishThread(threading.Thread):
	def __init__(self, urls):
		self.urls = urls
		threading.Thread.__init__(self)
	
	def run(self):
		quick_publish(*self.urls)

def refresh():
	urls = []

	runners = Runner.people.all()
	for runner in runners:
		urls.append(runner)

	meets = Meet.objects.all()
	for meet in meets:
		urls.append(meet)

	urls = urls + ['/meets/','/runners/','/top10/']

	QuickPublishThread(urls).start()

def menu_edit(request, id):
	response =  change_stage(request,'simplemenu','menu', id)

	if request.POST:
		refresh()

	return response

def menu_add(request):
	response =  add_stage(request,'simplemenu','menu')

	if request.POST:
		refresh()

	return response

def menu_delete(request, id):
	response =  delete_stage(request,'simplemenu','menu', id)

	if request.POST:
		refresh()

	return response

def menu_item_edit(request, id):
	response =  change_stage(request,'simplemenu','menuitem', id)

	if request.POST:
		refresh()

	return response

def menu_item_add(request):
	response =  add_stage(request,'simplemenu','menuitem')

	if request.POST:
		refresh()

	return response

def menu_item_delete(request, id):
	response =  delete_stage(request,'simplemenu','menuitem', id)

	if request.POST:
		refresh()

	return response
