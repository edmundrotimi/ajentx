
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#Admin settings
admin.site.site_header = 'Admin Area'
admin.site.site_title = 'Ajentx Admin'
admin.site.index_title= 'Ajentx Administration'
admin.empty_value_display= '**Empty**'

urlpatterns = [
    #admin document
    path(f'{settings.ADMIN_PATH}/doc/', include('django.contrib.admindocs.urls')),
    # admin path
    path(f'{settings.ADMIN_PATH}/', admin.site.urls),
    path(f'{settings.ADMIN_PATH}/doc/', include('django.contrib.admindocs.urls')),
    #honeypot
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('accounts/', include('accounts.urls')),
    path('account/', include('profiles.urls')),
    path('agents/', include('agents.urls')),
    path('listings/', include('listings.urls')),
    path('', include('pages.urls')),
    path('blog/', include('blog.urls')),
    path('contact/', include('contact.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
