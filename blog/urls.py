from .views import BlogList, BlogDetail 
from django.urls import path


urlpatterns = [
    path('post/', BlogList.as_view(), name='post_list'),
    path('post/<slug:slug>/', BlogDetail.as_view(), name='post_details'),
]
