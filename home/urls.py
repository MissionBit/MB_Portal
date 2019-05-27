from django.urls import path
from . import views


urlpatterns = [
		path('', views.home, name='home-home'),
		path('staff/', views.staff, name='home-staff'),
		path('student/', views.student, name='home-student'),
		path('teacher/', views.teacher, name='home-teacher'),
		path('volunteer/', views.volunteer, name='home-volunteer'),
]