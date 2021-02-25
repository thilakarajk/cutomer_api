from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^customers/(?P<pk>[0-9]+)$',
        views.GetDeleteUpdateCustomer.as_view(),
        name='get_delete_update_customer'
    ),
    url(
        r'^customers/$',
        views.GetPostCustomer.as_view(),
        name='get_post_customer'
    )
]
