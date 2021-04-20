from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'status']


admin.site.register(UserProfile, UserProfileAdmin)
