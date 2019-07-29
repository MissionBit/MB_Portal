from django.urls import path, include
from . import views

urlpatterns = [path("", views.student, name="student"),
               path("download_form/", views.download_form, name="download_form")]
