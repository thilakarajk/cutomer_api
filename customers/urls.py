from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^customers/(?P<pk>[0-9]+)$',
        views.get_delete_update_customer,
        name='get_delete_update_customer'
    ),
    url(
        r'^customers/$',
        views.get_post_customer,
        name='get_post_customer'
    )
]
