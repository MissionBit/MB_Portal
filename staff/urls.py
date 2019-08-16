from django.urls import path
from . import views

urlpatterns = [
    path("", views.staff, name="staff"),
    path(
        "classroom_management/", views.classroom_management, name="classroom_management"
    ),
    path("create_staff_user/", views.create_staff_user, name="create_staff_user"),
    path("create_teacher_user/", views.create_teacher_user, name="create_teacher_user"),
    path("create_student_user/", views.create_student_user, name="create_student_user"),
    path(
        "create_volunteer_user",
        views.create_volunteer_user,
        name="create_volunteer_user",
    ),
    path("create_classroom/", views.create_classroom, name="create_classroom"),
    path(
        "create_class_offering/",
        views.create_class_offering,
        name="create_class_offering",
    ),
    path("make_announcement/", views.make_announcement, name="make_announcement"),
    path("post_form/", views.post_form, name="post_form"),
    path("create_esign", views.create_esign, name="create_esign"),
    path("form_overview", views.form_overview, name="form_overview"),
    path(
        "notify_unsubmitted_users",
        views.notify_unsubmitted_users,
        name="notify_unsubmitted_users",
    ),
    path(
        "communication_manager/",
        views.communication_manager,
        name="communication_manager",
    ),
    path("curriculum/", views.curriculum, name="curriculum"),
    path("modify_session/", views.modify_session, name="modify_session"),
    path("add_forum/", views.add_forum, name="add_forum"),
    path("classroom_detail/<course_id>", views.classroom_detail, name="classroom_detail"),
]
