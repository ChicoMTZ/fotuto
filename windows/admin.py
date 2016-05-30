from django.contrib import admin
from windows.models import Window


class WindowAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'order')
    list_filter = ('active',)
    prepopulated_fields = {
        'slug': ('title',)
    }

admin.site.register(Window, WindowAdmin)
