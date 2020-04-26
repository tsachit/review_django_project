from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    readonly_fields = ['token']

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('id', 'username', 'get_token', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('id', 'username', 'profile__token', 'email', 'first_name', 'last_name', 'is_staff')
    list_display_links = ('id', 'username')
    list_select_related = ('profile', )
    list_per_page = 25

    def get_token(self, instance):
        return instance.profile.token
    get_token.short_description = 'User Token'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)