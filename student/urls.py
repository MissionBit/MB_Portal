from django.urls import path, include
from . import views

urlpatterns = [path("", views.student, name="student"),
               path("attendance_student/", views.attendance_student, name="attendance_student"),
               path("my_class_student/", views.my_class_student, name="my_class_student"),
               path("session_view_student/", views.session_view_student, name="session_view_student")]
