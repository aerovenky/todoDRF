from django.contrib import admin
from .models import Label, Note
# Register your models here.

class LabelDetail(admin.ModelAdmin):
    list_display = ('id','user','name',)

admin.site.register(Label, LabelDetail)

class NoteDetail(admin.ModelAdmin):
    list_display = ('id','user','name','body',)

admin.site.register(Note, NoteDetail)
