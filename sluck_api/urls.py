from django.conf.urls import url, include
from rest_framework import routers
from sluck_api import views

# router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^message/$', views.get_message, name='get_message'),
    url(r'^user/$', views.get_user, name='get_user'),
    url(r'^group/$', views.get_group, name='get_group'),
    url(r'^message/group/$', views.post_message, name='post_message'),
    url(r'^messages/group/$', views.get_group_messages, name='get_group_messages'),
    url(r'^message/like/$', views.like_message, name='like_message'),
    url(r'^message/dislike/$', views.dislike_message, name='dislike_message'),
    url(r'^message/reactions/$', views.get_reactions, name='message_reactions')
]