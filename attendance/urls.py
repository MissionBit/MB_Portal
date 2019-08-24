from django.urls import path
from . import views

urlpatterns = [
    path("", views.attendance, name="attendance"),
    path(
        "take_attendance/<course_id>/<date>/",
        views.take_attendance,
        name="take_attendance",
    ),
    path(
        "notify_absent_students/",
        views.notify_absent_students,
        name="notify_absent_students",
    ),
]
