from django.contrib import admin
from .models import *

class ImageInline (admin.TabularInline):
    model = Image
    extra = 0

class LinkInline(admin.TabularInline):
    model = Link
    extra = 0

class NoteAdmin(admin.ModelAdmin):
    list_display = ('uid','wallet','twitter','is_wl','is_viewed','only_twitter',)
    search_fields = ('uid','wallet','twitter',)
    list_filter = (
        'is_wl','is_viewed','is_forever','only_twitter',
    )
    model = Note

    # def get_textt(self, obj):
    #
    #     return obj.text[:20]
    #
    # get_textt.short_description = "text"
    inlines = [ImageInline, LinkInline]

class DaoRequestAdmin(admin.ModelAdmin):
    list_display = ('code', 'twitter', 'dao_twitter',)
    search_fields = ('twitter', 'dao_twitter',)
    model = DaoRequest

admin.site.register(Note,NoteAdmin)
admin.site.register(DaoCode)
admin.site.register(DaoRequest,DaoRequestAdmin)
admin.site.register(Captcha)
admin.site.register(SentCaptcha)
admin.site.register(Vote)
admin.site.register(VoteTeam)
admin.site.register(VoteTeamUser)

