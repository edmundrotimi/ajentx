from django.contrib import admin, messages
from reversion.admin import VersionAdmin
from .models import Contact


class AdminContact(VersionAdmin, admin.ModelAdmin):
    list_display = ['fullname', 'email', 'phone_number', 'date_created']
    list_display_links = ['fullname', 'email', 'phone_number']
    date_hierarchy = 'date_created'
    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    save_as = False
    save_as_continue = False
    save_on_top = True
    search_fields = ['fullname', 'email', 'phone_number', 'message', 'date_created']
    fields = ['fullname', 'email', 'phone_number', 'message', 'date_created']


admin.site.register(Contact, AdminContact)
