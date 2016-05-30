from django.contrib import admin
from mimics.models import Mimic, Rule


class RuleAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'var', 'min', 'max')


class MimicAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'window', 'x', 'y', 'width', 'height', 'graphic_type')
    filter_horizontal = ('vars', 'rules')

admin.site.register(Mimic, MimicAdmin)
admin.site.register(Rule, RuleAdmin)
