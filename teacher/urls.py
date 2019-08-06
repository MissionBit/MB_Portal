from django.urls import path, include
from . import views

urlpatterns = [path("", views.teacher, name="teacher"),
               path("my_class/", views.my_class, name="my_class"),
               path("session_view/", views.session_view, name="session_view")]
