from django.contrib import admin
from simplemenu.models import MenuItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    pass
