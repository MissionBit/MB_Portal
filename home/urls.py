from django.urls import path, include
from . import views


urlpatterns = [
		path('', views.landing_page, name='home-landing_page'),
		path('staff/', views.staff, name='home-staff'),
		path('student/', views.student, name='home-student'),
		path('teacher/', views.teacher, name='home-teacher'),
		path('volunteer/', views.volunteer, name='home-volunteer'),
		path('logout/', views.logout, name='home-logout'),
		path('register/', views.register, name='home-register'),
		path('home/', views.home, name='home-home'),
		path('register_as_student/', views.register_as_student, name='home-register_as_student'),
		path('register_as_volunteer/', views.register_as_volunteer, name='home-register_as_volunteer'),
		path('login/', include('django.contrib.auth.urls'))
]