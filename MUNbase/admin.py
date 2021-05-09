from django.contrib import admin

# Register your models here.
from .models import User, Experience, MUNuser, MUNannouncements, Registrations, Article
admin.site.register(User)
admin.site.register(Experience)
admin.site.register(MUNuser)
admin.site.register(MUNannouncements)
admin.site.register(Registrations)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'author', 'date')

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

admin.site.register(Article, ArticleAdmin)
