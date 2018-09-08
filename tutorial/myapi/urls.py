from django.urls import re_path, path
from myapi import views

urlpatterns = [
    path('student', views.student_list),
    re_path(r'^student/(?P<pk>[0-9]+)/$', views.student_detail)
]
