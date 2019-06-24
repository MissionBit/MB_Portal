from django.urls import path
from . import views

urlpatterns = [
        path('', views.staff, name='staff'),
        path('user_management/', views.user_management, name='user_management'),
        path('create_staff_user', views.create_staff_user, name='create_staff_user'),
        path('create_teacher_user', views.create_teacher_user, name='create_teacher_user'),
        path('create_student_user', views.create_student_user, name='create_student_user'),
        path('create_volunteer_user', views.create_volunteer_user, name='create_volunteer_user'),
        path('my_account_staff/', views.user_management, name='my_account_staff'),
        path('create_classroom/', views.create_classroom, name='create_classroom')
]
