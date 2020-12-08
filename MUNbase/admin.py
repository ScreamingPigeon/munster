from django.contrib import admin

# Register your models here.
from .models import User, Experience
admin.site.register(User)
admin.site.register(User,Experience)
