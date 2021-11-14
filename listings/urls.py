from django.urls import path
from . import views as view

urlpatterns = [
    path('create/', view.CreateListings.as_view(), name='create_listings'),
    path('update/<slug:slug>/', view.UpdateListings.as_view(),
         name='update_listings'),
    path('update/details/<slug:slug>/',
         view.ListingsUpdateDetails.as_view(), name='update_detail_listings'),
    path('error/', view.ListingsError.as_view(), name='listing_error'),
    path('<slug:slug>/delete/', view.DeleteListing.as_view(), name='delete_listing'),
    path('', view.Listings.as_view(), name='listings'),
    path('<slug:slug>/', view.ListingDetails.as_view(), name='listing_detail'),

]
