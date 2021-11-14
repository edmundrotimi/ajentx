from django.urls import path
from .views import (
    AccountSuspendedView, account_logout,
    AccountSuspension, AccountSignIn,
    AccountSignUp, revisiondelete
)


urlpatterns = [
    path('logout/', account_logout, name='logout'),
    path('suspension/', AccountSuspension.as_view(), name='account_suspend'),
    path('login/', AccountSignIn.as_view(), name='signin'),
    path('signup/', AccountSignUp.as_view(), name='signup'),
    path('reision/delete', revisiondelete, name="rev_delete"),
    path('user/lockedout/', AccountSuspendedView.as_view(), name='accountSuspended'),
]
