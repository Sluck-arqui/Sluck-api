from django.conf.urls import url, include
from rest_framework import routers
from sluck_api import views
from django.views.decorators.csrf import csrf_exempt

# router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^message/$', csrf_exempt(views.messages.get_message), name='get_message'),
    url(r'^message/group/$', csrf_exempt(views.messages.post_message), name='post_message'),
    url(r'^message/like/$', csrf_exempt(views.messages.like_message), name='like_message'),
    url(r'^message/dislike/$', csrf_exempt(views.messages.dislike_message), name='dislike_message'),
    url(r'^message/reactions/$', views.messages.get_reactions, name='message_reactions'),
    url(r'^message/comment/$', csrf_exempt(views.messages.post_comment), name='post_comment'),

    url(r'^search/hashtag/$', views.searches.search_hashtag, name='search_hashtag'),
    url(r'^search/username/$', views.searches.search_username, name='search_username'),

    url(r'^user/$', csrf_exempt(views.users.get_user), name='get_user'),

    url(r'^group/$', csrf_exempt(views.groups.get_group), name='get_group'),
    url(r'^group/new/$', csrf_exempt(views.groups.new_group), name='new_group'),
    url(r'^group/member/$', csrf_exempt(views.groups.group_member), name='group_member')
]