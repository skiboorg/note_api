from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *




class UserAdmin(BaseUserAdmin):
    list_display = (
        'email',
        'twitter',
        'is_in_wl',
        'fk_wl_1',
        'fk_wl_2',

    )
    ordering = ('id',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                "email",
                       'password1',
                       'password2',
                       ), }),)
    search_fields = ('id','email','code' )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info',
         {'fields': (


             'twitter',
             'wallet',
                "avatar",
                "is_in_wl",
             "code"

         )}
         ),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups',)}),)

class CodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_used', 'is_unlimited',)
    search_fields = ('code',)
    model = Code


admin.site.register(User, UserAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(PasswordForm)





