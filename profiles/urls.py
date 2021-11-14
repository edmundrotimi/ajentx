from django.urls import path
from .views import CreateProfile, ProfileDetail, UpdateProfile, DeleteProfile


urlpatterns = [
    path('profile/<slug:slug>/delete/',
         DeleteProfile.as_view(), name='profile_delete'),
    path('profile/<slug:slug>/update/',
         UpdateProfile.as_view(), name='profile_update'),
    path('profile/<slug:slug>/', ProfileDetail.as_view(), name='profile_details'),
    path('create/profile/', CreateProfile.as_view(), name='profile_create'),
]
