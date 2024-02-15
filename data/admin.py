from django.contrib import admin
from .models import *

class ImageInline (admin.TabularInline):
    model = Image
    extra = 0

class LinkInline(admin.TabularInline):
    model = Link
    extra = 0

class NoteAdmin(admin.ModelAdmin):
    list_display = ('uid','wallet','twitter','get_textt','is_wl','is_viewed')
    search_fields = ('uid','wallet','twitter',)
    list_filter = (
        'is_wl','is_viewed','is_forever'
    )
    model = Note

    def get_textt(self, obj):
        return obj.text[:20]

    get_textt.short_description = "text"
    inlines = [ImageInline, LinkInline]


admin.site.register(Note,NoteAdmin)

