from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.RewardsView.as_view(), name='rewards'),
    # url(r'^new_orders$', views.NewOrderView.as_view(), name='post-new-orders'),
]
