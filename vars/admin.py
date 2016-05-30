from django.contrib import admin
from .models import Var, Device


class VarAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'active', 'device', 'var_type', 'value', 'units')

admin.site.register(Device)
admin.site.register(Var, VarAdmin)
