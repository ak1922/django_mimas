from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AccountUser


class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type',)}),
    )
    list_display = UserAdmin.list_display + ('user_type',)
    list_per_page = 6

admin.site.register(AccountUser, CustomUserAdmin)
