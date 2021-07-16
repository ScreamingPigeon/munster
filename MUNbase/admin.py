from django.contrib import admin
from django import forms

# Register your models here.
from .models import User, Experience, MUNuser, MUNannouncements, Registrations, Delwatchlist, MUNwatchlist, Article, Committee, Participant, CommitteeAdmin, Talklist,TalkListSpeaker, Motion, Voter, Paperwork, Ammendment
admin.site.register(User)
admin.site.register(Experience)
admin.site.register(MUNuser)
admin.site.register(MUNannouncements)
admin.site.register(Committee)
admin.site.register(Participant)
admin.site.register(CommitteeAdmin)
admin.site.register(TalkListSpeaker)
admin.site.register(Talklist)
admin.site.register(Motion)
admin.site.register(Voter)
admin.site.register(Paperwork)
admin.site.register(Admin)

class ArticleEditorAdmin(forms.ModelForm):
    content = forms.CharField( widget=forms.Textarea )
    class Meta:
        model = Article
        fields ='__all__'
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    form = ArticleEditorAdmin

admin.site.register(Article, ArticleAdmin)
