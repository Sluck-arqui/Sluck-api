from django.conf.urls import url, include
from rest_framework import routers
from sluck_api import views

# router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^message/', views.get_message, name='get_message'),
    url(r'^user/', views.get_user, name='user')
]