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

class VoteAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'only_one_team','vote_price','time_left',)
    model = Vote

class VoteTeamAdmin(admin.ModelAdmin):
    list_display = ('vote', 'name', 'votes',)
    model = Vote


class VoteTeamUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'votes',)
    model = VoteTeamUser

class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject',

'email',
'tw',
'created_at',)
    model = Ticket

admin.site.register(Note,NoteAdmin)
admin.site.register(DaoCode)
admin.site.register(DaoRequest,DaoRequestAdmin)
admin.site.register(Captcha)
admin.site.register(SentCaptcha)
admin.site.register(Vote,VoteAdmin)
admin.site.register(VoteTeam,VoteTeamAdmin)
admin.site.register(VoteTeamUser,VoteTeamUserAdmin)
admin.site.register(Stats)
admin.site.register(MintImage)
admin.site.register(MintSettings)
admin.site.register(Ticket,TicketAdmin)

