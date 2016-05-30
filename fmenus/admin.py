from django.contrib import admin

from .models import MenuItem


class MenuItemAdmin(admin.ModelAdmin):
    # TODO: Show the icon in list_display
    list_display = ('__unicode__', 'position', 'text', 'mode', 'order', 'home', 'active')
    list_editable = ('order',)
    list_filter = ('position', 'active')

admin.site.register(MenuItem, MenuItemAdmin)
