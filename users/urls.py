from os import name

from django.conf.urls import url

from .views import (CreateUserAPIView, UserRetrieveUpdateAPIView,
                    authenticate_user)

urlpatterns = [
    url(r'^create/$', CreateUserAPIView.as_view(), name="create_user"),
    url(r'^update/$', UserRetrieveUpdateAPIView.as_view(), name="fetch_user"),
    url(r'^obtain_token/$', authenticate_user, name="authenticate_user"),
]
