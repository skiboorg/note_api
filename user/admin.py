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
             'claims',

         )}
         ),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups',)}),)

class CodeAdmin(admin.ModelAdmin):
    readonly_fields = ('use_count',)

    list_display = ('code', 'is_used', 'is_unlimited','use_count')
    search_fields = ('code',)
    list_filter = ('is_used', 'is_unlimited',)
    model = Code

    def use_count(self, obj):
        return User.objects.filter(code=obj.code).count()

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('uid','from_user', 'to_user', 'amount', 'created_at')
    search_fields = ('uid','from_user__uid','to_user__uid','amount','from_user__email','to_user__email')
    model = Transaction

class ClaimHistoryAdmin(admin.ModelAdmin):
    list_display = ('user','amount', 'created_at',)
    search_fields = ('user',)
    model = ClaimHistory

class WalletAdmin(admin.ModelAdmin):
    list_display = ('wallet','wl', 'wl1', 'wl2',)
    search_fields = ('wallet',)
    model = Wallet

class CoinUpgradeAdmin(admin.ModelAdmin):
    list_display = ('name','price', 'limit_add','click_add', )
    model = CoinUpgrade

class ClaimUpgradeAdmin(admin.ModelAdmin):
    list_display = ('name','price', 'claim_add' )
    model = ClaimUpgrade

admin.site.register(User, UserAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(PasswordForm)
admin.site.register(ClaimHistory,ClaimHistoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Wallet,WalletAdmin)
admin.site.register(CoinUpgrade,CoinUpgradeAdmin)
admin.site.register(UserCoinsUpgrade)
admin.site.register(UserClaimUpgrade)
admin.site.register(ClaimUpgrade,ClaimUpgradeAdmin)





