from django.contrib import admin
from .models import *


class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'date','program', 'gpa', 'gre')
    list_filter = ('user', 'date')
    search_fields = ('user__username', 'program')
    ordering = ('-date',) # Enable autocomplete for the user field

    
    
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'ranking', 'acceptance_rate', 'avg_gre', 'avg_gpa')
    list_filter = ('location', 'ranking')
    search_fields = ('name', 'location')
    ordering = ('ranking',)
    
admin.site.register(UserData, UserDataAdmin)
admin.site.register(University, UniversityAdmin)