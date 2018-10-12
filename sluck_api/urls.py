from django.conf.urls import url, include
from rest_framework import routers
from sluck_api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'messages', views.MessageViewSet)
router.register(r'thread_messages', views.ThreadMessageViewSet)
router.register(r'hashtags', views.HashtagViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^rest/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^register/$', views.register, name='register'),
    url(r'^user/$', views.get_user, name='get_user'),
    url(r'^group/$', views.get_group, name='get_group'),
    url(r'^group/new/$', views.new_group, name='new_group'),
    url(r'^group/member/$', views.group_member, name='group_member'),
    url(r'^message/$', views.get_message, name='get_message'),
    url(r'^message/group/$', views.post_message, name='post_message'),
    url(r'^message/like/$', views.like_message, name='like_message'),
    url(r'^message/dislike/$', views.dislike_message, name='dislike_message'),
    url(r'^message/reactions/$', views.get_message_reactions, name='message_reactions'),
    url(r'^message/comment/$', views.post_comment, name='post_comment'),
    url(r'^message/comment/like/$', views.like_thread, name='like_thread'),
    url(r'^message/comment/dislike/$', views.dislike_thread, name='dislike_thread'),
    url(r'^message/comment/reactions/$', views.get_thread_reactions, name='thread_reactions'),
    url(r'^search/hashtag/$', views.search_hashtag, name='search_hashtag'),
    url(r'^search/username/$', views.search_username, name='search_username'),
]
