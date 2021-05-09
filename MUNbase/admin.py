from django.contrib import admin
from django import forms

# Register your models here.
from .models import User, Experience, MUNuser, MUNannouncements, Registrations, Article
admin.site.register(User)
admin.site.register(Experience)
admin.site.register(MUNuser)
admin.site.register(MUNannouncements)
admin.site.register(Registrations)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    form = ArticleEditorAdmin
class ArticleEditorAdmin(forms.ModelForm):
    content = forms.CharField( widget=forms.Textarea )
    class Meta:
        model = Article

admin.site.register(Article, ArticleAdmin)
