from django.contrib import admin, messages
from reversion.admin import VersionAdmin
import admin_thumbnails
from .models import Profile


def unpublish_post(modeladmin, request, queryset):
    if queryset.filter(publish=True):
        queryset.update(publish=False)
    else:
        queryset.update(publish=True)
    messages.add_message(request, messages.SUCCESS,
                         'Selected post published/unpublished successfully.')


unpublish_post.short_description = 'Publish/Unpublish Post'


@admin_thumbnails.thumbnail('picture')
class AdminProfile(VersionAdmin, admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'company_name', 'country',
                    'state', 'city', 'status', 'publish']
    list_display_links = ['first_name', 'last_name', 'company_name', 'country',
                          'state', 'city', 'status', 'publish']
    list_filter = ['publish', ]
    date_hierarchy = 'last_updated'
    list_per_page = 50
    view_on_site = True
    actions = [unpublish_post]
    actions_on_top = True
    actions_on_bottom = True
    view_on_site = True
    save_as = True
    save_as_continue = True
    save_on_top = True
    search_fields = ['first_name', 'last_name', 'user', 'country',
                     'state', 'city', 'bio', 'publish', 'last_updated']
    fieldsets = [
        ['Account Info', {
            'fields': ['user', 'first_name', 'last_name']
        }],
        ['Profile Details', {
            'classes': ['collapse'],
            'fields': ['country', 'state', 'city', 'phone_number', 'company_name', 'status']
        }],
        ['Media', {
            'classes': ['collapse'],
            'fields': ['picture_thumbnail']
        }],
        ['Bio', {
            'classes': ['collapse'],
            'fields': ['bio']
        }],
        ['Timeline', {
            'classes': ['collapse'],
            'fields': ['publish', 'last_updated']
        }],
    ]


admin.site.register(Profile, AdminProfile)
