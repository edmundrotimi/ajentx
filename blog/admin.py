from django.contrib import admin, messages
from reversion.admin import VersionAdmin
import admin_thumbnails
from .models import BlogPost, BlogComment


def unpublish_post(modeladmin, request, queryset):
    if queryset.filter(publish=True):
        queryset.update(publish=False)
    else:
        queryset.update(publish=True)
    messages.add_message(request, messages.SUCCESS,
                         'Selected post published/unpublished successfully.')


unpublish_post.short_description = 'Publish/Unpublish Post'


@admin_thumbnails.thumbnail('feature_image',)
@admin_thumbnails.thumbnail('author_image',)
class BlogPostAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ['user', 'title', 'category', 'tags', 'publish']
    list_display_links = ['user', 'title', 'category', ]
    list_filter = ['publish', 'category']
    date_hierarchy = 'last_updated'
    list_per_page = 50
    actions = [unpublish_post]
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True
    search_fields = ['user', 'title', 'category', 'tags', 'detail', 'publish']
    fields = ['user', 'title', 'feature_image', 'category', 'tags',
              'detail', 'author_image', 'publish', 'last_updated']


admin.site.register(BlogPost, BlogPostAdmin)


class BlogCommentAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ['user', 'full_name', 'email', 'subject', 'publish']
    list_display_links = ['user', 'full_name', 'email', 'subject', ]
    list_filter = ['publish']
    date_hierarchy = 'last_updated'
    list_per_page = 50
    actions = [unpublish_post]
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True
    search_fields = ['user', 'full_name', 'email',
                     'subject', 'message', 'publish', 'last_updated']


admin.site.register(BlogComment, BlogCommentAdmin)
