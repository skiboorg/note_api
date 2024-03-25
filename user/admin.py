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
        'balance',
        'code',
        'can_claim',
        'date_joined'

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
    search_fields = ('id','email','code','twitter','wallet', )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info',
         {'fields': (


             'twitter',
             'wallet',
                "avatar",
                "is_in_wl",
             'fk_wl_1',
             'fk_wl_2',
             "code",
             "balance",
             'can_claim',
             'errors',
             'blocked',

         )}
         ),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups',)}),)

class CodeAdmin(admin.ModelAdmin):
    readonly_fields = ('use_count',)

    list_display = ('code', 'is_used', 'is_unlimited','use_count')
    search_fields = ('code',)
    list_filter=('is_used', 'is_unlimited',)
    model = Code

    def use_count(self, obj):
        return User.objects.filter(code=obj.code).count()


admin.site.register(User, UserAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(PasswordForm)





