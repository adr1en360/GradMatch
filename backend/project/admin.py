from django.contrib import admin
from .models import *


class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'date','program', 'gpa', 'gre', 'experience')
    list_filter = ('user', 'date')
    search_fields = ('user__username', 'program')
    ordering = ('-date',) # Enable autocomplete for the user field

    
admin.site.register(UserData, UserDataAdmin)