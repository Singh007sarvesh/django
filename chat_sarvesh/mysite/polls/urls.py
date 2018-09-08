from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('foo', views.foo),
    path('api/question', views.get_all_question),
    path('api/question/<int:question_id>', views.get_question),
    path('questions/<int:question_id>', views.question_votes),
    path('questions', views.display_all_question),
]
