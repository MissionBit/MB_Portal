from django.urls import path
from . import views

urlpatterns = [path("", views.attendance, name="attendance"),
               path("take_attendance/", views.take_attendance, name="take_attendance")]
