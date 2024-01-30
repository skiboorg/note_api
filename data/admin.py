from django.contrib import admin
from .models import *

class ImageInline (admin.TabularInline):
    model = Image
    extra = 0

class LinkInline(admin.TabularInline):
    model = Link
    extra = 0

class NoteAdmin(admin.ModelAdmin):
    model = Note
    inlines = [ImageInline, LinkInline]


admin.site.register(Note,NoteAdmin)

