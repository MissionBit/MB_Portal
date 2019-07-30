from django.urls import path, include
from . import views

urlpatterns = [path("", views.student, name="student"),
               path("download_form_student/", views.download_form_student, name="download_form_student")]
