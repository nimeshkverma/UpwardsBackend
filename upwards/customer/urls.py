from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^customer/$', views.CustomerList.as_view(), name='customer_list'),
    url(r'^customer/(?P<pk>[0-9]+)/$',
        views.CustomerDetail.as_view(), name='customer_detail'),
]
