from django.conf.urls import url
from snippets import views
from django.conf.urls import include

urlpatterns = [
    url(r'^snippets/$', views.snippet_list),
    url(r'^snippets/api/$', views.SnippetList.as_view()),
    url(r'^users/api/$', views.UserList.as_view()),
    url(r'^users/api/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^snippets/api/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
    url(r'^api-auth/', include('rest_framework.urls')),
]
