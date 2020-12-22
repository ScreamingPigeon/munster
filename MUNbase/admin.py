from django.contrib import admin

# Register your models here.
from .models import DelUser, Experience
admin.site.register(DelUser)
admin.site.register(Experience)
