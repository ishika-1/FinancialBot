from django.contrib import admin

# Register your models here.

from .models import UserDetails
admin.site.register(UserDetails)
