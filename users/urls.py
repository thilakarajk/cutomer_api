from os import name

from django.conf.urls import url

from .views import (AuthenticateUser, CreateUserAPIView,
                    UserRetrieveUpdateAPIView)

urlpatterns = [
    url(r'^create/$', CreateUserAPIView.as_view(), name="create_user"),
    url(r'^update/$', UserRetrieveUpdateAPIView.as_view(), name="fetch_user"),
    url(r'^obtain_token/$', AuthenticateUser.as_view(), name="authenticate_user"),
]
