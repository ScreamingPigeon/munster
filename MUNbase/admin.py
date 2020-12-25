from django.contrib import admin

# Register your models here.
from .models import User, Experience, MUNuser, MUNannouncements, Registrations
admin.site.register(User)
admin.site.register(Experience)
admin.site.register(MUNuser)
admin.site.register(MUNannouncements)
