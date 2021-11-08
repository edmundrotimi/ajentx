
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
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('account/', include('profiles.urls'))
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
