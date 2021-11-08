from django.urls import path
from .views import AccountSuspension, AccountSignIn, AccountSignUp


urlpatterns = [
    path('suspension/', AccountSuspension.as_view(), name='account_suspend'),
    path('login/', AccountSignIn.as_view(), name='signin'),
    path('signup/', AccountSignUp.as_view(), name='signup'),
]
