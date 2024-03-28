from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *




class UserAdmin(BaseUserAdmin):
    list_display = (
        'email',
        'twitter',
        'uid',
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
    search_fields = ('id','email','code','twitter','wallet', 'uid',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info',
         {'fields': (

            'uid',
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

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'amount', 'created_at')
    search_fields = ('from_user__uid','to_user__uid','amount','from_user__email','to_user__email')
    model = Transaction


admin.site.register(User, UserAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(PasswordForm)
admin.site.register(Transaction, TransactionAdmin)





