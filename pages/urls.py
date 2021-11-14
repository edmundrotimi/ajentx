from .views import HomeView, ServiceView, Faq
from django.urls import path

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('services/', ServiceView.as_view(), name='service'),
    path('faq/', Faq.as_view(), name='faq'),
]
