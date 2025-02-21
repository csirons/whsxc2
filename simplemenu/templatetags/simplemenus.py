from django import template
from simplemenu.models import Menu
from django.utils.safestring import mark_safe

register = template.Library()

def flatmenu(menuslug=None,cururl=None):
	menu = Menu.objects.get(slug=menuslug)
	menuitems = menu.menuitem_set.all()

	if len(menuitems) < 1:
		return ""

	m = '<ul id="%s-menu" class="flat-menu">' % menuslug
	for mi in menuitems:
		m = m + '<li><a href="%s" title="%s"' % (mi.url, mi.description)
		if cururl == mi.url:
			m = m + ' class="current"'

		m = m + '>%s</a></li>' % mi.title

	m = m + '</ul>'
	return mark_safe(m)

register.simple_tag(flatmenu)
