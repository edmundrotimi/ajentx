from django.contrib import admin, messages
from reversion.admin import VersionAdmin
import admin_thumbnails
from .models import PropertyListings


def unpublish_post(modeladmin, request, queryset):
    if queryset.filter(publish=True):
        queryset.update(publish=False)
    else:
        queryset.update(publish=True)
    messages.add_message(request, messages.SUCCESS,
                         'Selected post published/unpublished successfully.')


unpublish_post.short_description = 'Publish/Unpublish Post'


@admin_thumbnails.thumbnail('feature_image_1',)
@admin_thumbnails.thumbnail('feature_image_2',)
@admin_thumbnails.thumbnail('feature_image_3',)
@admin_thumbnails.thumbnail('gallery_image_1',)
@admin_thumbnails.thumbnail('gallery_image_2',)
@admin_thumbnails.thumbnail('gallery_image_3',)
class AdminPropertyListings(VersionAdmin, admin.ModelAdmin):
    list_display = ['id', 'property_name', 'country', 'year_built', 'property_status',
                    'property_category', 'property_size', 'property_price', 'publish']
    list_display_links = ['id', 'property_name', 'country', 'year_built', 'property_status',
                          'property_category', 'property_size', 'property_price']
    list_filter = ['publish', 'property_status']
    date_hierarchy = 'last_updated'
    list_per_page = 50
    actions = [unpublish_post]
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True
    search_fields = ['id', 'property_name', 'property_description', 'rooms', 'bedrooms',
                     'bathrooms', 'garage', 'garage_size', 'year_built', 'property_status',
                     'property_category', 'property_size', 'property_price', 'country', 'state',
                     'city', 'nearby', 'postal_code', 'neighborhood']
    fieldsets = [
        ['General Info', {
            'fields': ['property_name', 'property_description', 'property_status', 'property_category']
        }],
        ['Property Details', {
            'classes': ['collapse'],
            'fields': ['rooms', 'bedrooms', 'bathrooms', 'garage', 'garage_size', 'year_built', 'property_price']
        }],
        ['Location/Amenities', {
            'classes': ['collapse'],
            'fields': ['amenities', 'address', 'country', 'state', 'city', 'nearby', 'postal_code', 'neighborhood']
        }],
        ['Featured Images', {
            'classes': ['collapse'],
            'fields': ['feature_image_1_thumbnail', 'feature_image_2_thumbnail', 'feature_image_3_thumbnail']
        }],
        ['Media', {
            'classes': ['collapse'],
            'fields': ['gallery_image_1_thumbnail', 'gallery_image_1_details',
                       'gallery_image_2_thumbnail', 'gallery_image_2_details', 'gallery_image_3_thumbnail', 'gallery_image_3_details']
        }],
        ['Timeline', {
            'classes': ['collapse'],
            'fields': ['last_updated', 'publish']
        }],
    ]


admin.site.register(PropertyListings, AdminPropertyListings)
