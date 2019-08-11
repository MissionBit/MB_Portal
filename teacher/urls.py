from django.urls import path, include
from . import views

urlpatterns = [path("", views.teacher, name="teacher"),
               path("my_class_teacher/", views.my_class_teacher, name="my_class_teacher"),
               path("session_view_teacher/", views.session_view_teacher, name="session_view_teacher")]
