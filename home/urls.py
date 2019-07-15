from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.landing_page, name="home-landing_page"),
    path("logout/", views.logout_view, name="home-logout"),
    path("register/", views.register, name="home-register"),
    path("home/", views.home, name="home-home"),
    path(
        "register_as_student/",
        views.register_as_student,
        name="home-register_as_student",
    ),
    path(
        "register_as_volunteer/",
        views.register_as_volunteer,
        name="home-register_as_volunteer",
    ),
    path("register_as_donor/", views.register_as_donor, name="home-register_as_donor"),
    path(
        "register_after_oauth/",
        views.register_after_oauth,
        name="home-register_after_oauth",
    ),
    path("login/", include("django.contrib.auth.urls")),
    path("change_pwd/", views.change_pwd, name="change_pwd"),
]
