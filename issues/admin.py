from django.contrib import admin
from .models import IssueStatus, IssueType, Settings


class IssueStatusAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']

class IssueTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']


def show_value(obj):
    if '(*)' in obj.name:
       return '****'
    return obj.value
show_value.short_description = 'value'

class SettingsAdmin(admin.ModelAdmin):
    list_display = ['name', show_value]
    ordering = ['name']


# Register your models here.
admin.site.register(IssueStatus, IssueStatusAdmin)
admin.site.register(IssueType, IssueTypeAdmin)
admin.site.register(Settings, SettingsAdmin)

