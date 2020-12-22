from django.contrib import admin

# Register your models here.
from .models import User, Experience
admin.site.register(User)
admin.site.register(Experience)

class Experience(admin.ModelAdmin):
    list_display = ('delegate', 'MUN', 'committee', 'year', 'position')
admin.site.register(Experience)
