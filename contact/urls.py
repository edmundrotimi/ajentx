from .views import Contact
from django.urls import path


urlpatterns = [
    path('', Contact.as_view(), name='user-contact'),
]
