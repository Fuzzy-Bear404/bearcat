from django.contrib import admin
from django.contrib.auth.models import User

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from django.utils.html import format_html
from django.contrib import messages

from .models import (
    MainPageContent, DropdownItem, Topic, Topic_title, 
    PageVisit, UserProfile
)

# Register your models here.


class DropdownItemInline(admin.TabularInline):
    model = DropdownItem
    extra = 1

@admin.register(MainPageContent)
class MainPageContentAdmin(admin.ModelAdmin):
    inlines = [DropdownItemInline]

admin.site.register(Topic)

admin.site.register(Topic_title)

@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'path', 'referer', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('ip_address', 'path', 'referer')


# ===== User Profile with Trusted Feature =====

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    
    fields = (
        'profile_image',
        'is_trusted',
        'trusted_since'
    )
    readonly_fields = ('trusted_since',)


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    
    list_display = [
        'username', 'email', 'first_name', 'last_name', 
        'is_staff', 'is_trusted_display', 'date_joined'
    ]
    
    list_filter = [
        'is_staff', 'is_superuser', 'is_active',
        'profile__is_trusted',
        'date_joined'
    ]
    
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    def is_trusted_display(self, obj):
        """Show trusted status"""
        if hasattr(obj, 'profile') and obj.profile.is_trusted:
            return format_html(
                '<span style="color: white; background: #007bff; padding: 3px 8px; '
                'border-radius: 3px; font-weight: bold;">⭐ TRUSTED</span>'
            )
        return format_html(
            '<span style="color: #666;">-</span>'
        )
    is_trusted_display.short_description = 'Trusted'


# Unregister default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Simplified UserProfile admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_trusted', 'trusted_since']
    list_filter = ['is_trusted']
    search_fields = ['user__username', 'user__email']
    
    readonly_fields = ['trusted_since']
    
    fieldsets = (
        ('User', {
            'fields': ('user', 'profile_image')
        }),
        ('Trusted Status', {
            'fields': ('is_trusted', 'trusted_since')
        }),
    )