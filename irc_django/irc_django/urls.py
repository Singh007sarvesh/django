"""irc_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from posts import views as core_views
from rest_framework.authtoken import views as view
from posts import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', core_views.signup, name="signup"),
    path('login_users', core_views.login_user),
    path('moderator', core_views.admin),
    path('messages/<int:channel_id>', core_views.display_message),
    re_path(r'^message/(?P<channel_id>[0-9]+)/$', core_views.message),
    path('logout/', core_views.logout_user),
    path('api/users', views.UserList.as_view()),
    re_path(r'^api/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    re_path(r'^api/channels/$', core_views.ChannelList.as_view()),
    re_path(r'^api/channels/(?P<pk>[0-9]+)/$',
            core_views.ChannelDetail.as_view()),
    re_path(r'^api/channels/(?P<pk>[0-9]+)/messages/$',
            core_views.MessageList.as_view()),
    re_path(r'^api/channels/(?P<pk>[0-9]+)/messages/(?P<msg_id>[0-9]+)/$',
            core_views.MessageDetail.as_view()),
    path('api/login/', view.obtain_auth_token),
    path('api/logout', views.Logout.as_view()),
]
